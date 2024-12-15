"""
This module handles data transformation processes for machine learning pipelines:

- Handles missing data using strategies like median and most frequent imputation.
- Scales numerical data and applies one-hot encoding to categorical data.
- Combines preprocessing pipelines using ColumnTransformer for efficient handling.
- Saves the preprocessing object as a .pkl file for future use.
"""


import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data__transformation__config = DataTransformationConfig()
    
    def get_data_transformer_object(self):
        """_summary_
        This function is responsible for data transformation 

        Raises:
            CustomException: _description_

        Returns:
            _type_: _description_
        """
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")), #Use median bcs there are some outliers
                    ("scaler", StandardScaler()),
                ]
            )
            

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False)),
                ]
            )

            logging.info(f"Numerical columns : {numerical_columns}")
            logging.info(f"Categorical columns : {categorical_columns}")

            preprocessor  = ColumnTransformer(
                [
                    ("numerical_pipeline", num_pipeline, numerical_columns),
                    ("categorical_pipeline", cat_pipeline, categorical_columns),
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e.sys)

    def initiate_data_transformation(self,train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info(f"Read train and test completed")

            logging.info(f"Obtaining preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()

            target_coloumn_name = 'math_score'
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df = train_df.drop(columns = [target_coloumn_name], axis = 1)
            target_feature_train_df = train_df[target_coloumn_name]

            input_feature_test_df=test_df.drop(columns = [target_coloumn_name],axis=1)
            target_feature_test_df=test_df[target_coloumn_name]

            logging.info(f"Applying prerpocessing object on training and testing df")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved processing object.")

            save_object(
                file_path = self.data__transformation__config.preprocessor_obj_file_path,
                obj = preprocessing_obj,
            )

            return (
                train_arr,
                test_arr,
                self.data__transformation__config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e,sys)