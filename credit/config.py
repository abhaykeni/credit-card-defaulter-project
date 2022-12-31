import sys,os
import pymongo
from dataclasses import dataclass
from credit.logger import logging
from credit.exception import CreditException

@dataclass
class EnvironmentVariables:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")


env_var = EnvironmentVariables()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)