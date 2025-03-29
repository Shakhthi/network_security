import sys
import os

import numpy as np
import pandas as pd
from typing import List

import pymongo
import certifi

from network_security.exception.exception_handler import NetworksecurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_config import DataIngestionArtifact

from sklearn.model_selection import train_test_split

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URI")

ca = certifi.where()

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info("Data Ingestion class is initialized")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworksecurityException(e, sys)
    def export_collection_as_dataframe(self):
        try:
            logging.info("Exporting collection as dataframe")
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na": np.nan}, inplace=True)

            logging.info("Exporting collection as dataframe is done")
            return df
        except Exception as e:
            raise NetworksecurityException(e, sys)
    
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            logging.info("Exporting data into feature store")

            dataframe = self.export_collection_as_dataframe()
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            logging.info("Exporting data into feature store is done")
            return dataframe     
        except Exception as e:
            raise NetworksecurityException(e, sys)
    
    def split_data_as_train_test(self, dataframe:pd.DataFrame):
        try:
            logging.info("Splitting data as train and test")
            train, test = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Splitting data as train and test is done")

            logging.info("Initiated saving train and test data into CSV")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"train file path: {os.path.dirname(dir_path)}")
            train.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info("Saving train and test data into CSV is done")

        except Exception as e:
            raise NetworksecurityException(e, sys)
        
    def initiate_data_ingestion(self):
        try:
            logging.info("Initiating data ingestion")
            df = self.export_collection_as_dataframe()
            df = self.export_data_into_feature_store(df)
            self.split_data_as_train_test(df)
            dataIngestionArtifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path=self.data_ingestion_config.testing_file_path)
            logging.info("Data ingestion is done")
            return dataIngestionArtifact
        except Exception as e:
            raise NetworksecurityException(e, sys)

