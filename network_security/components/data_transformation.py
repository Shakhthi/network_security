import sys
import os

import numpy as np
import pandas as pd

from network_security.exception.exception_handler import NetworksecurityException
from network_security.logging.logger import logging

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constant.training_pipeline import (
    TARGET_COLUMN,
    DATA_TRANSFORMATION_IMPUTER_PARAMS,
)

from network_security.entity.artifact_config import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
from network_security.entity.config_entity import DataTransformationConfig
from network_security.utils.main_utils.utils import (
    save_numpy_array_data,
    save_object,
)

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            logging.info("Data Transformation class constructor instantiated.")
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworksecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:

        try:
            logging.info(f"Reading the data from {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworksecurityException(e, sys)
    
    def get_data_transformer_object(self):
        try:
            logging.info("Creating data transformer object")
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            processor:Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworksecurityException(e, sys)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("initiate_data_transformation method called")
            logging.info("Reading the train and test data")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)


            logging.info("Reading Train and test data")
            # train dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            #test dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            logging.info("preprocessor object creation initiated.")
            preprocessor = self.get_data_transformer_object()

            logging.info("fitting and transforming the train and test data")
            transformed_input_train_feature = preprocessor.fit_transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
            test_arr = np.c_[ transformed_input_test_feature, np.array(target_feature_test_df) ]

            logging.info("Saving the transformed train and test data as .npy files")
            #save numpy array data
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor)

            save_object( "final_model/preprocessor.pkl", preprocessor)

            logging.info("data transformation artifact created.")
            #preparing artifacts
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact

        except Exception as e:
            raise NetworksecurityException(e, sys)

