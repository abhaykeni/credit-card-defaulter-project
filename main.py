from credit.pipeline.training_pipeline import start_training_pipeline
from credit.pipeline.batch_prediction_pipeline import start_bath_prediction_pipeline



if __name__=="__main__":
   try:
      start_training_pipeline()
      #start_bath_prediction_pipeline(input_file_path="/config/workspace/Credit_Card.csv")

   except Exception as e:
      print(e)
          