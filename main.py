from credit.logger import logging
from credit.exception import CreditException
from credit.components.data_ingestion import DataIngestion
from credit.entity import config_entity


if __name__=="__main__":
     try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
                   
     except Exception as e:
        raise CreditException(e,sys)
          