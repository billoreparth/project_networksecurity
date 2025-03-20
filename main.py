import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("intiate data ingetion process")

        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
    except Exception as e :
        raise TypeError(NetworkSecurityException(e,sys))