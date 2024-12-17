import os
import sys

import numpy as np
import pandas as pd
import dill
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import r2_score

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    



def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}

        for model_name, model in models.items():

            param = params.get(model_name, {})  # Safely get parameters for the current model

            # Train the model
            if param:
                # Perform GridSearchCV for hyperparameter tuning
                gs = GridSearchCV(model, param, cv=3, n_jobs=-1)
                gs.fit(X_train, y_train)
                model = gs.best_estimator_  # Get the best model from GridSearch
            else:
                # Directly fit the model if no parameters are provided
                model.fit(X_train, y_train)

            best_model = gs.best_estimator_  # Use best_estimator_ for simplicity
            best_model.fit(X_train, y_train)

            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)
            
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score
        
        return report
    
    
    except Exception as e:
        raise CustomException(e, sys)
    
