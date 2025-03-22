from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import os,sys
import pandas as pd 

class DataValidation:
    def __init__(self,
                 data_validation_config:DataValidationConfig):
        
        try:
            # self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_column=len(self._schema_config)
            logging.info('validation of number of column intialize')
            if len(dataframe.columns)==number_of_column:
                return True
            return False
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def validate_numeric_column(self,dataframe:pd.DataFrame)->bool:
        try:
            num_column=[i for i in dataframe.columns if i.dtype != 'O']
            if len(num_column) == 0:
                return False
            return True 
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = "D:/Work/NLP & ML/NetworkSecurity/Artifacts/09_16_2024_20_37_54/data_ingestion/ingested/train.csv"
            test_file_path = "D:/Work/NLP & ML/NetworkSecurity/Artifacts/09_16_2024_20_37_54/data_ingestion/ingested/test.csv"
            # reading these files 
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)
            # validating number of dataframe 
            status=self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = "train data has not equal column"
            status =self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = "test data has not equal column"
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path="D:/Work/NLP & ML/NetworkSecurity/Artifacts/09_16_2024_20_37_54/data_validation/validated/train.csv",
                valid_test_file_path="D:/Work/NLP & ML/NetworkSecurity/Artifacts/09_16_2024_20_37_54/data_validation/validated/test.csv",
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=None,
            )

            return data_validation_artifact

        
        except Exception as e :
            raise NetworkSecurityException(e,sys)