from credit.entity import config_entity,artifact_entity
from credit.logger import logging
from credit.exception import CreditException
from credit import utils
import sys,os


class DataValidation:
    def __init__(self,data_validation_config:config_entity.DataValidationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise CreditException(e,sys)

    

    def initiate_data_validation():
        try:
            pass
        except Exception as e:
            raise CreditException(e,sys)
