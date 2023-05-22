import pandas as pd
import json
import os
from credit.config import mongo_client,UPLOAD_FOLDER


data_base_list = os.listdir(UPLOAD_FOLDER)

BASE_FILE_PATH = os.path.join(UPLOAD_FOLDER,data_base_list[len(data_base_list)-1])
DATABASE_NAME = "score"
COLLECTION_NAME = "credit"

def data_dumpy():
    #Read csv file
    df = pd.read_csv(BASE_FILE_PATH)
    print(df.shape)
    #Reset file index
    df.reset_index(drop=True,inplace=True)

    #Convert pandas data frame to JSON
    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])
    # Insert into MongoDB
    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)

