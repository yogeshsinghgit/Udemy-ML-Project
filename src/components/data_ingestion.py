
import os, sys
import pandas as pd
from typing import List
from src.logger import logging
from dataclasses import dataclass
from src.exception import CustomException
from sklearn.model_selection import train_test_split

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

# stores the file path for input to another files

@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join('artifacts', 'train.csv')
    test_data_path:str = os.path.join('artifacts', 'test.csv')
    raw_data_path:str = os.path.join('artifacts', 'data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        '''
        reads data from databases or any file path
        '''
        logging.info("Data Ingestion Method Running")
        
        try:
            df = pd.read_csv('notebook\data\stud.csv')
            logging.info("Dataset is readed as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index = False, header=True)

            logging.info("Train Test Split Initiated...")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state= 42)

            train_set.to_csv(self.ingestion_config.train_data_path, index = False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index = False, header=True)
        
            logging.info("data ingestion completed.")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data  = obj.initiate_data_ingestion()
    
    # data transformation code
    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)


