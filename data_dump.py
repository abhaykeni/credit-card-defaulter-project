import pandas as pd
import json
from credit.config import mongo_client


BASE_FILE_PATH = "/config/workspace/Credit_Card.csv"
DATABASE_NAME = "score"
COLLECTION_NAME = "credit"


if __name__=="__main__":
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

