
import os, sys

import numpy as np
import pandas as pd

from dataclasses import dataclass

from sklearn.model_selection import train_test_split

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


## the config file is created just to provide file path to other classes and methods.
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''to create all pkl file of perprocessing'''
        try:
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            logging.info("Creating Pipelines")

            num_pipeline = Pipeline(steps= [
                ("imputer", SimpleImputer(strategy='mean')),
                ('Scaler', StandardScaler())
            ])

            cat_pipelne = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy='most_frequent')),
                ("OHEncoding", OneHotEncoder())     
            ])

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ('cat_pipeline', cat_pipelne, categorical_columns)
                ]
            )

            logging.info("Pipelines are Created")

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("train and test data reading completed")

            logging.info("preprocessing initiated")
            preprocessor_obj = self.get_data_transformer_object()

            target_column_name =  "math_score"

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis = 1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis = 1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Appliying Preprocessing on training and testing dataset")

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            # https://stackoverflow.com/questions/10894323/what-does-the-c-underscore-expression-c-do-exactly
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]
            
            logging.info("Preporcessed objects are Saved")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)


