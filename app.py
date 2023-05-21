from credit.pipeline.training_pipeline import start_training_pipeline
from credit.pipeline.batch_prediction_pipeline import start_bath_prediction_pipeline
from distutils.log import debug
from fileinput import filename
from werkzeug.utils import secure_filename
import pandas as pd
from flask import Flask, request, jsonify
import data_dump
import os 

UPLOAD_FOLDER = os.path.join('staticfiles', 'uploads') 

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
 
# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def uploadFile():
   if request.method == 'POST':
      # upload file flask
      for file in os.listdir(UPLOAD_FOLDER):
         os.remove(os.path.join(UPLOAD_FOLDER,file))

      f = request.files.get('file')
 
      # Extracting uploaded file name
      data_filename = secure_filename(f.filename)
 
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],data_filename))
 
      return render_template('index2.html')
   return render_template("index.html")
 

@app.route('/train',methods=['GET','POST'])
def train():
   if request.method == 'POST':
      print(request.form.get('train'))
      if request.form.get('train') == 'train':
            print("Inside Training")
            data_dump.data_dumpy()
            start_training_pipeline()
            return render_template("train.html") 
   return render_template('index2.html')
    

@app.route('/predict',methods=['GET','POST'])
def predict():
   if request.method == 'POST':
      if request.form.get('predict') == 'predict':
            print("Inside Prediction")
            start_bath_prediction_pipeline(input_file_path="/config/workspace/Credit_Card.csv")
            return render_template("predict.html")
   return render_template("index2.html")

 
@app.route('/show_data')
def showData():
   # Uploaded File Path
   data_file_path = ""
   #session.get('uploaded_data_file_path', None)
   # read csv
   uploaded_df = pd.read_csv(data_file_path,encoding='unicode_escape')
   # Converting to html Table
   uploaded_df_html = uploaded_df.to_html()
   return render_template('show_csv_data.html',data_var=uploaded_df_html)

if __name__=="__main__":
   try:
      app.run(debug=True)
   except Exception as e:
      print(e)
          