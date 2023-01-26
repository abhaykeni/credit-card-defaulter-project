from credit.logger import logging
from credit.exception import CreditException
from credit.entity import config_entity, artifact_entity
from credit import utils
import pandas as pd
import numpy as np
import os,sys
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CreditException(e,sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info("Exporting data from database as DataFrame")
            df:pd.DataFrame = utils.get_collection_as_dataframe(
                database_name = self.data_ingestion_config.database_name, 
                collection_name = self.data_ingestion_config.collection_name)

            logging.info("Replace na values with NAN")
            df.replace(to_replace="na",value=np.NAN,inplace=True)

            logging.info("Make dir for storing feature data")
            feature_store_dir = os.path.dirname(p=self.data_ingestion_config.feature_store_file_path)
            os.makedirs(name=feature_store_dir,exist_ok=True)

            logging.info("Save feature as csv to feature file path")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            logging.info("Split feature data into training data and testing data")
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)

            logging.info("Make dir for storing train and test data")
            dataset_dir = os.path.dirname(p=self.data_ingestion_config.train_file_path)
            os.makedirs(name=dataset_dir,exist_ok=True)

            logging.info("Save train data as csv to train file path")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            logging.info("Save test data as csv to test file path")
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)

            logging.info("Preparing Data Ingestion Artifact")

            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path = self.data_ingestion_config.feature_store_file_path, 
                train_file_path = self.data_ingestion_config.train_file_path, 
                test_file_path = self.data_ingestion_config.test_file_path )

            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise CreditException(e,sys)
