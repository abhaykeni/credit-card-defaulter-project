from credit.pipeline.training_pipeline import start_training_pipeline
from credit.pipeline.batch_prediction_pipeline import start_bath_prediction_pipeline
from credit.config import UPLOAD_FOLDER
from werkzeug.utils import secure_filename
import pandas as pd
from flask import *
import dbpush
import os 


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def uploadFile():
   try:
      if request.method == 'POST':
         for file in os.listdir(UPLOAD_FOLDER):
            os.remove(os.path.join(UPLOAD_FOLDER,file))

         f = request.files.get('file')
         data_filename = secure_filename(f.filename)
         f.save(os.path.join(app.config['UPLOAD_FOLDER'],data_filename))
   
         return render_template('index2.html')
      return render_template("index.html")
   except Exception as e:
      print(e)

 

@app.route('/train',methods=['GET','POST'])
def train():
   try:
      if request.method == 'POST':
         print(request.form.get('train'))
         if request.form.get('train') == 'train':
               print("Inside Training")
               dbpush.data_dumpy()
               start_training_pipeline()
               return render_template("train.html") 
      return render_template('index2.html')
   except Exception as e:
      raise(e)
      

@app.route('/predict',methods=['GET','POST'])
def predict():
   try:
      if request.method == 'POST':
         if request.form.get('predict') == 'predict':
               data_file_list = os.listdir(UPLOAD_FOLDER)
               data_file_path = os.path.join(UPLOAD_FOLDER,data_file_list[len(data_file_list)-1])
               start_bath_prediction_pipeline(input_file_path=data_file_path)
               return render_template("predict.html")
      return render_template("index2.html")
   except Exception as e:
      print(e)

 
@app.route('/show_data')
def showData():
   try:
      data_file_list = os.listdir(os.path.join(os.getcwd(),"prediction"))
      data_file_path = os.path.join(os.getcwd(),"prediction",data_file_list[len(data_file_list)-1])
      uploaded_df = pd.read_csv(data_file_path,encoding='unicode_escape')
      return send_file(data_file_path,as_attachment=True)
   except Exception as e:
      print(e)

if __name__=="__main__":
   try:
      app.run(debug=True)
   except Exception as e:
      print(e)
          