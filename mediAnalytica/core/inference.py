import torch
from torchvision import transforms
import pickle
import numpy as np
from PIL import Image
import os 
import json
from django.conf import settings
from typing import List

class InferenceService:
    def __init__(self):
        rf_model_path = r"core/weights/symptom_rf.sav"
        json_file_path = os.path.join(settings.BASE_DIR, 'data', 'symptoms.json')
        torch_lung_model_path = r"core/weights/lungmodel.pth"
        with open(rf_model_path, 'rb') as file :
            self.rf_model = pickle.load(file)

        with open(json_file_path, 'r') as file:
            self.SYMPTOMS_DICT = json.load(file)

        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.model = torch.load(torch_lung_model_path, map_location=torch.device('cpu'))
        self.model.eval()

    def predict_disease_from_symptom(self, symptoms: List)->str:
        x = np.zeros((1,132))
        for symptom in symptoms:
            if symptom in self.SYMPTOMS_DICT:
                x[0][self.SYMPTOMS_DICT[symptom]] = 1

        prediction = self.rf_model.predict(x)[0]
        return prediction
    
    def segment_lungs(self, image: Image.Image)->Image.Image:
        image_tensor = self.transform(image).unsqueeze(0)  
        with torch.no_grad():
            output = self.model(image_tensor)
        # output_img = torch.permute(torch.squeeze(output, 0), (1, 2, 0)).numpy()
        output_arr = output[0][0].numpy().astype(int)
        print(f'Generated Mask of shape {output_arr.shape}')
        op_image = Image.fromarray(output_arr, mode='L')
        return op_image

