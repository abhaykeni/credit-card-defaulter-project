import pandas as pd
import numpy as np
import os,sys
import dill
import yaml
from credit.logger import logging
from credit.exception import CreditException
from credit.config import mongo_client



def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame():
    try:
        logging.info("Extracting data from database:{database_name} and collection:{collection_name}")
        mongo_data = mongo_client[database_name][collection_name].find()
        df = pd.DataFrame(mongo_data)
        if "_id" in df.columns:
            df.drop(columns="_id",inplace=True)
        return df
    except Exception as e:
        raise CreditException(e,sys)

def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise SensorException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise CreditException(e, sys) from e


def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CreditException(e, sys) from e


def write_yaml_file(file_path:str,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,'w') as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise CreditException(e,sys)




