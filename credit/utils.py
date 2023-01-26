import pandas as pd
import numpy as np
import os,sys
import dill
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

def save_numpy_array_data(file_path:str,array:np.arr):
    try:
        dir_path = os.path.dirname(p=file_path)
        os.makedirs(name=dir_path,exist_ok=True)
        with open (file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise CreditException(e,sys)

def load_numpy_array_data(file_path:str):
    try:
        with open (file_path,"rb") as file_obj:
            np.load(file_obj)
    except Exception as e:
        raise CreditException(e,sys)


def save_object(file_path:str,obj=object):
    try:
        logging.info("Entered the save_object method of MainUtils class")
        dir_path = os.path.dirname(p=file_path)
        os.makedirs(name=dir_path,exist_ok=True)
        with open (file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise CreditException(e,sys)

def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CreditException(e,sys)




