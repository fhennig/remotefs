from flask import Flask
from flask import request
import os.path


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "data"


@app.route('/', methods=['POST'])
def file_io():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'ERROR'
        file = request.files['file']
        if 'filename' not in request.form:
            return 'ERROR 2'
        filename = request.form['filename']
        print("Saving file: {}".format(filename))
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        ensure_dir(full_path)
        file.save(full_path)
        return 'OK'
