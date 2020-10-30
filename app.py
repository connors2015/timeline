from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import render_template
from client import Client
import os
import time

UPLOAD_FOLDER = '/static/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


client = Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/<string:filename>')
def run_upload(filename):
    #file = open('file.txt', 'r')    
    upload = client.upload_to_ipfs(filename)
    link = client.view_on_web_client(upload)
    return render_template('viewer.html', link = link)

@app.route('/server_connect/')
def connect_to_post_server():
    client.connect_post_server()
    string = 'Connected!'
    return render_template('index.html', connected = string)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    if request.method == 'POST':
        if file.filename == '':
            flash('No selected file')
            string = 'No file selected file'
            return render_template('index.html', connected = string)


        if file and allowed_file(file.filename): 
            file.save('./static/' + secure_filename(file.filename))

            while not os.path.exists('./static/' + secure_filename(file.filename)):
                time.sleep(1)
           
            if os.path.isfile('./static/' + secure_filename(file.filename)):
                try:
                    print('upload_start')
                    upload = client.upload_to_ipfs(file.filename)
                    while upload == None:
                        time.sleep(1)
                    print('uploaded')
                    link = client.view_on_web_client(upload)
                except:
                    string = 'error uploading to IPFS'
                    #if os.path.exists('./static/' + secure_filename(file.filename)):
                    #    os.remove('./static/' + secure_filename(file.filename))
                    return render_template('index.html', connected = string)

    
    
    if os.path.exists('./static/' + secure_filename(file.filename)):
        os.remove('./static/' + secure_filename(file.filename))

    return render_template('viewer.html', link=link)



def main():
    app.run()


if __name__ == "__main__":
    main()