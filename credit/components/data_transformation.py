from credit.entity import config_entity, artifact_entity
from credit.logger import logging
from credit.exception import CreditException
import os,sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from imblearn.combine import SMOTETomek
from credit.config import TARGET_COLUMN
from credit import utils



class DataTransformation:
    def __init__(self, data_transformation_config=config_entity.DataTransformationConfig,
        data_ingestion_artifact=artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise CreditException(e,sys)

    def initiate_data_transformation(self)->artifact_entity.DataTransformationArtifact:
        try:
            logging.info("Importing Train and Test Data as a DataFrame")
            train_df = pd.read_csv(filepath_or_buffer=self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(filepath_or_buffer=self.data_ingestion_artifact.test_file_path)

            logging.info("Creating Input Feature for Train and Test Dataset")
            input_feature_train_df = train_df.drop(TARGET_COLUMN,axis=1) 
            input_feature_test_df = test_df.drop(TARGET_COLUMN,axis=1)

            logging.info("Creating Target Feature for Train and Test Dataset")
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            logging.info("Running Robustscaler on Input Train Features")
            transformation_pipeline = RobustScaler()
            transformation_pipeline.fit(X=input_feature_train_df)

            logging.info("Transforming Input Train and Test Features")
            input_feature_train_arr = transformation_pipeline.transform(X=input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(X=input_feature_test_df)

            logging.info("Converting target dataframe to array")
            target_feature_train_arr = target_feature_train_df.to_numpy()
            target_feature_test_arr = target_feature_test_df.to_numpy()

            smt = SMOTETomek(random_state=42)

            logging.info(f"Before Re-Sampling in Train Set: Input {input_feature_train_arr.shape} and Output: {target_feature_train_arr.shape}")
            input_feature_train_arr , target_feature_train_arr = smt.fit_resample(X=input_feature_train_arr, y=target_feature_train_arr)
            logging.info(f"After Re-Sampling in Training Set: Input {input_feature_train_arr.shape} and Output: {target_feature_train_arr.shape}")

            logging.info(f"Before Re-Sampling in Test Set: Input {input_feature_test_arr.shape} and Output: {target_feature_test_arr.shape}")
            input_feature_test_arr , target_feature_test_arr = smt.fit_resample(X=input_feature_test_arr, y=target_feature_test_arr)
            logging.info(f"After Re-Sampling in Test Set: Input {input_feature_test_arr.shape} and Output: {target_feature_test_arr.shape}")

            logging.info("Merging input feature array and target array")
            train_arr = np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr,target_feature_test_arr]

            logging.info("Saving numpy train array and test array data ")
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path, array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path, array=test_arr)

            logging.info("Saving transformer object")
            utils.save_object(file_path=self.data_transformation_config.transform_object_path,obj=transformation_pipeline)

            logging.info("Preparing Data Transformation Artifact")
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path= self.data_transformation_config.transform_object_path, 
                transformed_train_path = self.data_transformation_config.transformed_train_path, 
                transformed_test_path = self.data_transformation_config.transformed_test_path
                )
            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
            
        except Exception as e:
            raise CreditException(e,sys)

