import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_ingestion import DataIngestion 
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("intiate data ingetion process")
        logging.info("completed data ingestion and started data validation process")
        datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
        data_validaton=DataValidation(datavalidationconfig)
        data_validation_artifact=data_validaton.initiate_data_validation()
        print(data_validation_artifact)

        # dataingestionartifact=data_ingestion.initiate_data_ingestion()
        
    except Exception as e :
        raise TypeError(NetworkSecurityException(e,sys))