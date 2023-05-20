from credit.entity import config_entity,artifact_entity
from credit.logger import logging
from credit.exception import CreditException
import sys,os
from credit.config import TARGET_COLUMN
from credit.predictor import ModelResolver
from credit.utils import load_object
import pandas as pd
from sklearn.metrics import f1_score, accuracy_score
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
            
            logging.info("Finding location of transformer model and target encoder")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()

            logging.info("Previous trained objects of transformer, model and target encoder")
            #Previous trained  objects
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)

            logging.info("Currently trained model objects")
            #Currently trained model objects
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model = load_object(file_path=self.model_trainer_artifact.model_path)

            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true = target_df.to_numpy()
            # accuracy using previous trained model

            input_feature_name = list(transformer.feature_names_in_)
            input_arr = transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            previous_model_score = accuracy_score(y_true=y_true,y_pred=y_pred)
            logging.info(f"Accuracy using previous trained model: {previous_model_score}")

            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr = current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            y_true = target_df.to_numpy()
            current_model_score = accuracy_score(y_true=y_true,y_pred=y_pred)
            logging.info(f"Accuracy using current trained model: {current_model_score}")

            if current_model_score<=previous_model_score:
                logging.info(f"Current trained model is not better than previous model")
                raise Exception("Current Trained Model is not better than previously trained model")

            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, 
            improved_accuracy=current_model_score-previous_model_score)
            logging.info(f"Model eval artifact: {model_eval_artifact}")
            return model_eval_artifact
            
        except Exception as e:
            raise CreditException(e,sys)
