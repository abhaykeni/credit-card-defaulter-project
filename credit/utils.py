import pandas as pd
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


