from credit.entity import config_entity,artifact_entity
from credit.config import TARGET_COLUMN
from credit.logger import logging
from credit.exception import CreditException
from scipy.stats import ks_2samp
from credit import utils
from typing import Optional
import sys,os
import pandas as pd
import numpy as np
import yaml


class DataValidation:
    def __init__(self,data_validation_config:config_entity.DataValidationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise CreditException(e,sys)

    def drop_missing_value_collumns(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            logging.info(f"Selecting Collumns names which contain null values above threshold: {threshold}")
            drop_column_names = null_report[null_report>threshold].index

            logging.info(f"List of Collumns to drop: {drop_column_names}")
            self.validation_error[report_key_name] = list(drop_column_names)
            df.drop(list(drop_column_names),axis=1,inplace=True)

            if len(df.columns) == 0:
                return None
            return df
        except Exception as e:
            raise CreditException(e,sys)

    def is_required_columns_exist(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns
            missing_collumns = []

            for column in base_columns:
                if column not in current_columns:
                    logging.info(f"Column: [{column} is not available.]")
                    missing_collumns.append(column)
            
            if len(missing_collumns)>0:
                self.validation_error[report_key_name]= list(missing_collumns)
                return False
            return True
        except Exception as e:
            raise CreditException(e,sys)

    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str,):
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for column in base_columns:
                base_data,current_data  = base_df[column],current_df[column]
                logging.info(f"Hypothesis {column}: {base_data.dtype}, {current_data.dtype} ")
                same_distribution =ks_2samp(base_data,current_data)

                if same_distribution.pvalue>0.5:
                    drift_report[column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    drift_report[column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }
            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise CreditException(e,sys)

    

    def initiate_data_validation(self):
        try:
            logging.info("Read base data frame")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na",np.NAN},inplace=True)
            logging.info("Replace NA values")

            logging.info("Drop Null values from base_df")
            base_df = self.drop_missing_value_collumns(df=base_df,report_key_name="Missing value columns in base dataset")

            logging.info("Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info("Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info("Drop Null values from train_df")
            train_df = self.drop_missing_value_collumns(df=train_df, report_key_name="Missing value columns in train dataset")
            logging.info("Drop Null values from test_df")
            test_df = self.drop_missing_value_collumns(df=test_df, report_key_name="Missing value columns in test dataset")

            exclude_columns = [TARGET_COLUMN]

            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exist(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.is_required_columns_exist(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")

            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=test_df,report_key_name="data_drift_within_test_dataset")

            
            logging.info("Write reprt in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise CreditException(e,sys)
