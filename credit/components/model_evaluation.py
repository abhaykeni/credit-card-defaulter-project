from credit.entity import config_entity,artifact_entity
from credit.logger import logging
from credit.exception import CreditException
import sys,os
from credit.config import TARGET_COLUMN
from credit.predictor import ModelResolver
from credit import utils
import pandas as pd
from sklearn.metrics import f1_score
import numpy as np



class ModelEvaluation:
    
    def __init__(self,
        model_evalution_config:config_entity.ModelEvaluationConfig,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Model Evaluation {'<<'*20}")
            self.model_evalution_config = model_evalution_config
            self.model_trainer_artifact = model_trainer_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise CreditException(e,sys)

    def initiate_model_evaluation(self):
        try:
            logging.info("if saved model folder has a model then we will compare whether"
            "current trained model is better than the previously saved model")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path == None:
                logging.info("Preparing Model Evaluation Artifact")
                model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, 
                improved_accuracy=None)
                logging.info(f"Model Evaluation Artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact
            
            logging.info("Find latest location of transformer and model")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            logging.info(f"Latest Transformer Path: {transformer_path}")
            model_path = self.model_resolver.get_latest_model_path()
            logging.info(f"Latest Model Path: {model_path}")

            logging.info("Importing previosly trained transformer and model")
            transformer = utils.load_object(file_path=transformer_path)
            model = utils.load_object(file_path=model_path)

            logging.info("Importing currently trained transformer and model")
            current_transformer = utils.load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model = utils.load_object(file_path=self.model_trainer_artifact.model_path)

            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            input_feature_df = test_df.drop(TARGET_COLUMN,axis=1)
            target_df = test_df[TARGET_COLUMN]
            y_true = target_df.to_numpy()

            logging.info("Prediction using previous model")
            input_feature_name = list(transformer.feature_names_in_)
            input_arr = transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            
            previous_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using previous model score:{previous_model_score}")

            logging.info("Predication using current model")
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr = current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)

            current_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using current model score: {current_model_score}")

            if current_model_score<=previous_model_score:
                logging.info("Current Trained Model is not better than Previous Trained Model")
                raise Exception("Current Trained Model is not better than Previous Trained Model")

            model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, 
            improved_accuracy=current_model_score-previous_model_score)
            logging.info(f"Model Evaluation Artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
            
        except Exception as e:
            raise CreditException(e,sys)
