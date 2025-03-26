import os
import sys

import numpy as np
import pandas as pd

"""
Defining common constant variable for training pipeline
"""

TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "Artifacts"  
FILE_NAME:str = "phisingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEME_FILE_PATH:str = os.path.join("data_schema", "schema.yaml")
SAVED_MODEL_DIR:str = os.path.join("saved_models")
MODEL_FILE_NAME:str = "model.pkl"

"""
Data ingestion constants starts with DATA_INGESTION var name

"""
DATA_INGESTION_COLLECTION_NAME:str = "NetworkData"
DATA_INGESTION_DATABASE_NAME:str = "MK"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:str = 0.2