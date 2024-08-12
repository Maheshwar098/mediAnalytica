import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image
import os
import torch
import torchvision
from torchvision import datasets, transforms, models
from typing import List, Tuple, Callable
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from torchvision.io import read_image
import ternausnet.models
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2 

def find_image_and_mask_paths(img_dir: str, mask_dir: str) -> Tuple[List[str], List[str], int]:
    """
    Scans the specified directories for images and corresponding masks.

    Args:
        img_dir (str): Directory containing the images.
        mask_dir (str): Directory containing the masks.

    Returns:
        Tuple[List[str], List[str], int]: 
            - List of image file paths.
            - List of mask file paths corresponding to the images.
            - Number of images for which masks were not found.
    """
    img_paths = []
    mask_paths = []
    mask_miss = 0

    for root, _, files in os.walk(img_dir):
        for file in files:
            img_name = file.split('.')[0]
            mask_name = img_name + "_mask"
            if os.path.exists(os.path.join(mask_dir, mask_name + ".png")):
                img_paths.append(os.path.join(root, file))
                mask_paths.append(os.path.join(mask_dir, mask_name + ".png"))
            else:
                mask_miss += 1

    return img_paths, mask_paths, mask_miss

class SegmentationDataset(Dataset):
    
    @staticmethod
    def preprocess_mask(mask):
        mask = mask = (mask != 0).astype(np.float32)  
        return mask
    
    def __init__(self, annotation_file: pd.DataFrame|str, img_dir:str, mask_dir:str, transform=None):
        if type(annotation_file)==str:
            self.df = pd.read_csv(annotation_file)
        else:
            self.df = annotation_file
        self.img_dir = img_dir
        self.mask_dir = mask_dir
        self.transform = transform

    def __len__(self):
        return self.df.shape[0]
    
    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.df.iloc[idx, 0])
        mask_path = os.path.join(self.mask_dir, self.df.iloc[idx, 1])
        #Albumentations only accepts Numpy arrays
        image = cv2.imread(img_path)
        mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED,)
#         print('cv2: ', image.shape, mask.shape)
        mask = self.preprocess_mask(mask)
        if self.transform:
            transform = self.transform(image=image, mask=mask)
            image = transform['image']
            mask = transform['mask']
#         print('albu:', image.shape, mask.shape)
        return image, mask

def prepare_datasets(
    df: pd.DataFrame,
    img_dir: str,
    mask_dir: str,
    transforms: List[Callable] = [],
    test_size: float = 0.1
) -> Tuple[SegmentationDataset, SegmentationDataset]:
    """
    Splits the dataset into training and validation sets, and prepares transformations and datasets.

    Args:
        df (pd.DataFrame): DataFrame containing image and mask paths.
        img_dir (str): Directory containing the images.
        mask_dir (str): Directory containing the masks.
        transforms (List[Callable], optional): List of additional transformations to apply to the images. Defaults to an empty list.
        test_size (float, optional): Proportion of the dataset to include in the validation split. Defaults to 0.1.

    Returns:
        Tuple[SegmentationDataset, SegmentationDataset]: 
            - Training dataset.
            - Validation dataset.
    """
    # Split DataFrame into training and validation sets
    df_train, df_val = train_test_split(df, test_size=test_size)

    # Define transformations for training and validation
    train_transforms = A.Compose([
        A.Resize(256, 256),
        *transforms,  # Unpack additional transformations
        A.Normalize(),
        ToTensorV2(),
    ])
    val_transforms = A.Compose([
        A.Resize(256, 256),
        A.Normalize(),
        ToTensorV2(),
    ])

    # Create datasets
    train_dataset = SegmentationDataset(df_train, img_dir, mask_dir, train_transforms)
    val_dataset = SegmentationDataset(df_val, img_dir, mask_dir, val_transforms)

    return train_dataset, val_dataset

def train(
    train_dataset,
    val_dataset,
    params: Dict[str, any]
) -> Tuple[List[float], List[float]]:
    """
    Trains a segmentation model with the given parameters and datasets.

    Args:
        train_dataset: Dataset for training.
        val_dataset: Dataset for validation.
        params (Dict[str, any]): Dictionary containing training parameters.
            - 'batch_size': Batch size for the DataLoader.
            - 'num_workers': Number of workers for DataLoader.
            - 'epochs': Number of training epochs.
            - 'device': 'cuda' or 'cpu' for device selection.
            - 'model_name': Name of the model to use.
            - 'learning_rate': Learning rate for the optimizer.

    Returns:
        Tuple[List[float], List[float]]: 
            - List of training losses for each epoch.
            - List of validation losses for each epoch.
    """
    BATCH_SIZE = params.get('batch_size', 16)
    NUM_WORKERS = params.get('num_workers', 2)
    EPOCHS = params.get('epochs', 10)
    DEVICE = torch.device(params.get('device', 'cuda') if torch.cuda.is_available() else 'cpu')
    MODEL_NAME = params.get('model_name', 'UNet11')
    LEARNING_RATE = params.get('learning_rate', 0.001)

    # Initialize model
    model = getattr(ternausnet.models, MODEL_NAME)(pretrained=True)
    model = model.to(DEVICE)

    # Data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=True,
    )

    # Loss function and optimizer
    criterion = torch.nn.BCEWithLogitsLoss().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    train_history = []
    val_history = []

    # Training loop
    model.to(DEVICE)
    for epoch in range(EPOCHS):
        print(f"Epoch {epoch}", end='')
        model.train()
        running_loss = 0.0
        for inputs, targets in train_loader:
            print("|", end='')
            inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(inputs).squeeze(1)
            assert outputs.shape == targets.shape, f"Shapes of output {outputs.shape} and target {targets.shape} do not match for input {inputs.shape}"
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        train_history.append(running_loss / len(train_loader))
        
        running_loss = 0.0
        model.eval()
        with torch.no_grad():
            for inputs, targets in val_loader:
                print("|", end='')
                inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
                outputs = model(inputs).squeeze(1)
                loss = criterion(outputs, targets)
                running_loss += loss.item()
            val_history.append(running_loss / len(val_loader))
        
        print(f" TrainLoss: {train_history[-1]}  ValLoss: {val_history[-1]}")

    return train_history, val_history

if __name__ == "__main__":
    # Define directories
    IMG_DIR = "/kaggle/input/chest-xray-masks-and-labels/Lung Segmentation/CXR_png/"
    MASK_DIR = "/kaggle/input/chest-xray-masks-and-labels/Lung Segmentation/masks"

    # Find image and mask paths
    img_paths, mask_paths, mask_miss = find_image_and_mask_paths(IMG_DIR, MASK_DIR)
    print(f"Found {len(img_paths)} images, {mask_miss} masks not found")

    # Create DataFrame from paths
    df = pd.DataFrame(data={'image': img_paths, 'mask': mask_paths})

    # Prepare datasets
    train_dataset, val_dataset = prepare_datasets(
        df,
        IMG_DIR,
        MASK_DIR,
        transforms=[A.HorizontalFlip(p=0.5), A.VerticalFlip(p=0.5)],  # Example transformations
        test_size=0.1
    )

    # Define training parameters
    params = {
        'batch_size': 16,
        'num_workers': 2,
        'epochs': 10,
        'device': 'cuda',
        'model_name': 'UNet11',
        'learning_rate': 0.001
    }

    # Train the model
    train_history, val_history = train(train_dataset, val_dataset, params)

    # Optionally, save or visualize the results
    print("Training history:", train_history)
    print("Validation history:", val_history)