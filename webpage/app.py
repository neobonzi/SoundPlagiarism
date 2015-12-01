import os
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
      print 'A'
      file = request.files['file']
      if file and allowed_file(file.filename):
         print 'B'
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         return redirect(url_for('uploaded_file',
                                 filename=filename)) 
   return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
   # change to call python subprocess synthesizer with arguments then present file
   return send_from_directory(app.config['UPLOAD_FOLDER'],
                              filename)

if __name__ == "__main__":
   app.run(debug=True)
