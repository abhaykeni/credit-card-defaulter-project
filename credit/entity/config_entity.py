import os,sys
from datetime import datetime
from credit.logger import logging
from credit.exception import CreditException

FEATURE_FILE_NAME = "credit.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"


class TrainingPipelineConfig:
    try:
        def __init__(self):
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
    except Exception as e:
        raise CreditException(e,sys)

class DataIngestionConfig:
    try:
        def __init__(self,training_pipeline_config:TrainingPipelineConfig):
            self.database_name = "score"
            self.collection_name = "credit"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FEATURE_FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.2
    except Exception as e:
        raise CreditException(e,sys)

class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...
