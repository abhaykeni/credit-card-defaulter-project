import sys,os
from datetime import datetime
from credit.logger import logging
from credit.exception import CreditException
from credit.predictor import ModelResolver
from credit import utils
import pandas as pd
import numpy as np

PREDICTION_DIR = "prediction"


def start_bath_prediction_pipeline(input_file_path):
    try:
        logging.info("Creating a prediction directory")
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info("Creating Model Resolver")
        model_resolver = ModelResolver()
        logging.info(f"Reading input file path: {input_file_path}")
        input_df = pd.read_csv(input_file_path)
        input_df.replace({"na":np.NAN},inplace=True)

        logging.info(f"Loading transformer to transform dataset")
        transformer = utils.load_object(file_path=model_resolver.get_latest_transformer_path())

        input_feature_names = list(transformer.feature_names_in_)
        input_arr = transformer.transform(input_df[input_feature_names])

        logging.info("Loading model for prediction")
        model = utils.load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)

        input_df["prediction"] = prediction

        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)

        input_df.to_csv(prediction_file_path,index=False,header=True)
        return prediction_file_path         
    except Exception as e:
        raise CreditException(e,sys)