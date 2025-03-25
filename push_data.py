import os
import sys
import json

import certifi 

import numpy as np
import pandas as pd
import pymongo
import pymongo.mongo_client 

from network_security.exception.exception_handler import NetworksecurityException
from network_security.logging.logger import logging

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URI")
print(MONGO_DB_URL)

ca = certifi.where()

class NetworkDataExtract:
    logging.info("NetworkDataExtract class is initialized")
    def __int__(self):
        try:
            pass
        except Exception as e:
            raise NetworksecurityException(e, sys)
        
    def csv_to_json_converter(self, file_path):
        try:
            logging.info("CSV to JSON conversion is started")
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())

            logging.info("CSV to JSON conversion is done")
            return records
            
        except Exception as e:
            raise NetworksecurityException(e, sys)
    
    def insert_data_mongodb(self, records, database, collection):
        try:
            logging.info("Inserting data into MongoDB")
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            logging.info("Data inserted into MongoDB")
            return len(self.records)
            
        except Exception as e:
            raise NetworksecurityException(e, sys)
        
if __name__ == '__main__':
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "MK"
    collection = "NetworkData"
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_converter(file_path=FILE_PATH)
    no_of_records = network_obj.insert_data_mongodb(records, DATABASE, collection)
    print(no_of_records)
