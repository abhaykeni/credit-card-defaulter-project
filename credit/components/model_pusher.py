from credit.entity import config_entity,artifact_entity
from credit.exception import CreditException
from credit.logger import logging
from credit import utils
from credit.predictor import ModelResolver
import sys,os


class ModelPusher:
    def __init__(self,model_pusher_config:config_entity.ModelPusherConfig,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        try:
            logging.info(f"{'>>'*20} Model Pusher {'<<'*20}")
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise CreditException(e,sys)

    def initiate_model_pusher(self):
        try:
            logging.info("Loading trained Transformer and model")
            transformer = utils.load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model = utils.load_object(file_path=self.model_trainer_artifact.model_path)

            logging.info("Save Transformer and Model to Model Pusher dir")
            utils.save_object(file_path=self.model_pusher_config.pusher_transformer_path,obj=transformer)
            utils.save_object(file_path=self.model_pusher_config.pusher_model_path,obj=model)

            logging.info("Save Transformer and Model to Saved Models dir")
            transformer_path = self.model_resolver.get_latest_save_transformer_path()
            model_path = self.model_resolver.get_latest_save_model_path()

            utils.save_object(file_path=transformer_path,obj=transformer)
            utils.save_object(file_path=model_path,obj=model)

            logging.info("Preparing Model Pusher Artifact")
            model_pusher_artifact = artifact_entity.ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir, 
            saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"Model Pusher Artifact: {model_pusher_artifact}")
            return model_pusher_artifact
            
        except Exception as e:
            raise CreditException(e,sys)
