import sys

from network_security.logging.logger import logging
from network_security.exception.exception_handler import NetworksecurityException

from network_security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
from network_security.components.data_validation import DataValidation
from network_security.entity.artifact_config import DataIngestionArtifact

from network_security.components.data_ingestion import DataIngestion

if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Initiation Completed")
        print(dataingestionartifact, sep='\n')
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data Validation Completed")
        print(data_validation_artifact)
    except Exception as e:
        raise NetworksecurityException(e, sys)