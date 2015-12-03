import os
import subprocess
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
from sklearn import svm
from tqdm import *
from pymongo import MongoClient
from pydub import AudioSegment
import sys
import numpy as np
import pickle
import granulizer
import analyzer
import subprocess
from flask import Flask, send_from_directory, render_template, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB limit

def allowed_file(filename):
   return '.' in filename and \
      filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      file = request.files['file']
      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         return redirect(url_for('uploaded_file',
                                 filename=filename)) 
   return render_template('index.html', data={})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
   client = MongoClient()
   db = client.audiograins
   grainEntries = db.grains
   song = AudioSegment.empty()
   songFile = open('./uploads/' + filename)
   print("converting to mono")
   monoFilename = "mono" + filename
   subprocess.check_call(["ffmpeg -i ./uploads/" + filename + " -ac 1 -threads 2 " + monoFilename], close_fds=True, shell=True)
   grains = granulizer.chopSound(monoFilename, 20, "inputGrains", "sample")
   labels = {"chorus" : 0, "hip-hop" : 0, "latin" : 0, "orchestra" : 0, "pop" : 0, "rock" : 0, "country" : 0, "jazz" : 0, "opera" : 0, "piano" : 0, "reggae" : 0, "techno" : 0}
   classifications = ["chorus", "hip-hop", "latin", "orchestra", "pop", "rock", "country", "jazz", "opera", "piano", "reggae", "techno"];
   totalGrains = 0;
   normalizer = pickle.load(open("normalizer.pickle"))
   classifier = pickle.load(open("classifier.pickle"))
   indextoIds = pickle.load(open("indexToIds.pickle"))

   for grain in tqdm(grains):
       totalGrains += 1
       dataPoint = np.empty([1, 16])
       mfccs = analyzer.analyzeMFCC(grain)
       dataPoint[0][0] = mfccs[0]
       dataPoint[0][1] = mfccs[1]
       dataPoint[0][2] = mfccs[2]
       dataPoint[0][3] = mfccs[3]
       dataPoint[0][4] = mfccs[4]
       dataPoint[0][5] = mfccs[5]
       dataPoint[0][6] = mfccs[6]
       dataPoint[0][7] = mfccs[7]
       dataPoint[0][8] = mfccs[8]
       dataPoint[0][9] = mfccs[9]
       dataPoint[0][10] = mfccs[10]
       dataPoint[0][11] = mfccs[11]
       dataPoint[0][12] = mfccs[12]
       dataPoint[0][13] = analyzer.analyzePitch(grain)
       dataPoint[0][14] = analyzer.analyzeEnergy(grain)
       dataPoint[0][15] = analyzer.analyzeZeroCrossingRate(grain)
       genreName = classifications[int(classifier.predict(normalizer.transform(dataPoint))[0])]
       labels[genreName] += 1

   for key in labels:
      labels[key] = str((float(labels[key]) / float(totalGrains)) * 100.0)
       
   subprocess.check_call(["rm -f ./inputGrains/*"], close_fds=True, shell=True)
   subprocess.check_call(["rm *.mp3"], close_fds=True, shell=True)
   subprocess.check_call(["rm ./uploads/*.mp3"], close_fds=True, shell=True)
   return render_template('index.html', data=labels)

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True, threaded=True)
