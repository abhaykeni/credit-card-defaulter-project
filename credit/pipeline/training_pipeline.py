import os,sys
from credit.logger import logging
from credit.exception import CreditException
from credit.components.data_ingestion import DataIngestion
from credit.components.data_validation import DataValidation
from credit.components.data_transformation import DataTransformation
from credit.components.model_trainer import ModelTrainer
from credit.components.model_evaluation import ModelEvaluation
from credit.components.model_pusher import ModelPusher
from credit.entity import config_entity

def start_training_pipeline():
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
        data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()
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
        model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
        model_pusher = ModelPusher(model_pusher_config=model_pusher_config, 
        data_transformation_artifact=data_transformation_artifact, 
        model_trainer_artifact=model_trainer_artifact)
        model_pusher_artifact = model_pusher.initiate_model_pusher()
    except Exception as e:
        raise CreditException(e,sys)
            
        