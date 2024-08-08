import numpy as np 
import pandas as pd 
import sklearn
from sklearn.ensemble import RandomForestClassifier
import pickle

from typing import List, Tuple
import os

def load_dataset(data_path: str)->Tuple[np.ndarray, np.ndarray]:
    """
    Load data from train.csv from data path and return X_train and Y_train
    """
    df = pd.read_csv(data_path)
    X_Train, Y_Train = df.drop(['prognosis', 'Unnamed: 133'], axis=1).values, df['prognosis'].values
    return X_Train, Y_Train

def train_model(x_train: np.ndarray, y_train: np.ndarray)->sklearn.base.BaseEstimator:
    assert x_train.shape[0]==y_train.shape[0], "Incorrect Shapes for data and labels"

    print(f"Training Model on data with {x_train.shape[0]} records and {x_train.shape[1]} features")
    model = RandomForestClassifier()
    model.fit(x_train, y_train)
    return model 

def save_model(model, save_path):
    with open(save_path, 'wb') as file:
        pickle.dump(model, file)
    file.close()
    print(f"Model saved successfully to {save_path}")

if __name__ == "__main__":
    DATA_PATH = r"data\train.csv"
    SAVE_PATH = r"core/static/symptom_rf.sav"

    X, Y = load_dataset(DATA_PATH)
    model = train_model(X, Y)
    save_model(model, SAVE_PATH)

