from credit.entity import config_entity,artifact_entity
from credit.exception import CreditException
from credit.logger import logging
import sys,os
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from credit import utils
from sklearn.metrics import f1_score



class ModelTrainer:
    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CreditException(e,sys)

    def hyperparemeter_tunning():
        try:
            pass
        except Exception as e:
            raise CreditException(e,sys)

    def train_model(self,X,y):
        try:
            model = XGBClassifier()
            model.fit(X,y)
            return model
        except Exception as e:
            raise CreditException(e,sys)

    def initiate_model_training(self):
        try:
            logging.info("Load numpy data for train and test data")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            logging.info("Split Data into input feature and target feature")
            X_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            X_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            logging.info('Training the model')
            model = self.train_model(X=X_train, y=y_train)

            logging.info('Calculating f1_score for training dataset')
            yhat_train = model.predict(X_train)
            f1_train_score = f1_score(y_true=y_train,y_pred=yhat_train)

            logging.info('Calculating f1_score for testing dataset')
            yhat_test = model.predict(X_test)
            f1_test_score = f1_score(y_true=y_test,y_pred=yhat_test)

            logging.info(f"Train score: {f1_train_score} and Test score: {f1_test_score}")

            logging.info("Check if model is underfitting")
            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {f1_test_score}")
            
            logging.info("Check if model is overfitting")
            diff = abs((f1_train_score-f1_test_score))

            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and Test Score Difference:{diff} is more than overfitting threshold:{self.model_trainer_config.overfitting_threshold}")

            logging.info("Save the object")
            utils.save_object(file_path=self.model_trainer_config.model_path,obj=model)

            logging.info("Preparing Model Trainer Artifact")
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
                f1_train_score=f1_train_score,f1_test_score=f1_test_score)
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise CreditException(e,sys)