import os,sys
from credit.logger import logging
from credit.exception import CreditException
from credit.components.data_ingestion import DataIngestion
from credit.components.data_transformation import DataTransformation
from credit.components.model_trainer import ModelTrainer
from credit.components.model_evaluation import ModelEvaluation
from credit.entity import config_entity


if __name__=="__main__":
     try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
        data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, 
        data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_training()  
        model_evalution_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_evaluation = ModelEvaluation(model_evalution_config=model_evalution_config,
        model_trainer_artifact=model_trainer_artifact, 
        data_transformation_artifact=data_transformation_artifact,
        data_ingestion_artifact=data_ingestion_artifact)
        model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
                        
     except Exception as e:
        raise CreditException(e,sys)
          