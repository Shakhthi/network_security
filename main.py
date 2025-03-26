import sys

from network_security.logging.logger import logging
from network_security.exception.exception_handler import NetworksecurityException

from network_security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
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
    except Exception as e:
        raise NetworksecurityException(e, sys)