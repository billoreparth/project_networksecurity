import os 
import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import (TrainingPipelineConfig,DataIngestionConfig,DataTransformationConfig,DataValidationConfig,ModelTrainerConfig)
from networksecurity.entity.artifact_entity import (ModelTrainerArtifact,DataIngestionArtifact,DataTransformationArtifact,DataValidationArtifact)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig

    def start_data_ingestion(self):
        try:
            logging.info("starting data ingestion process")
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion=DataIngestion(self.data_ingestion_config)
            dataingestionartifact=data_ingestion.initiate_data_ingestion()
            return dataingestionartifact
        except Exception as e :
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info("starting data validation process")
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            datavalidationartifact=data_validation.initiate_data_validation()
            return datavalidationartifact
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            logging.info("starting data transformation process")
            data_trasformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation=DataTransformation(data_transformation_config=data_trasformation_config,data_validation_artifact=data_validation_artifact)
            datatransformationartifact=data_transformation.intiate_data_transformation()
            return datatransformationartifact
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifact:ModelTrainerArtifact):
        try:
            logging.info("starting model trainer")
            model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer=ModelTrainer(model_transformation_artifact=data_transformation_artifact,model_trainer_config=model_trainer_config)
            modeltrainerartifact=model_trainer.intiate_model_trainer()
            return modeltrainerartifact
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def run_pipeline(self):
        try:
            dataingestionartifact=self.start_data_ingestion()
            datavalidationartifact=self.start_data_validation(data_ingestion_artifact=dataingestionartifact)
            datatransformationartifact=self.start_data_transformation(data_validation_artifact=datavalidationartifact)
            modeltrainerartifact=self.start_model_trainer(data_transformation_artifact=datatransformationartifact)
            return modeltrainerartifact 
            # return "done"
        except Exception as e :
            raise NetworkSecurityException(e,sys)