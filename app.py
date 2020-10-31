from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import render_template
from client import Client
from time_enums import TimeBlockCategories
from entry import Entry
import os
import time

UPLOAD_FOLDER = '/static/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'flac'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#for the love of god please setup ssh keys.
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


client = Client()

@app.route('/')
def index():
    return render_template('index.html', time = time.ctime(), connected = client.isConnected)

@app.route('/new_post/', methods=['POST', 'GET'])
def upload_new_post():

    server = '1.1.1.1'
    title  = request.form['title']
    url = request.form['url']
    print(title, url)

    entry = Entry(TimeBlockCategories.MISC, url)
    #run upload file and retrieve IPFS hash and IPFS web hash
    file = request.files['file']
    if file.filename != '':
        hashed_link, web_link = upload_file(request.files['file'])
        entry.set_ipfs_id(hashed_link) 
        entry.set_title(title)

        try:
            check_submission = client.upload_to_submission_server(entry, server)
        except:
            print('Failed to submit post to server.')
            ##need to return to somewhere for errors.

        return render_template('viewer.html', link=web_link, connected = client.isConnected, time = time.ctime())
    else:
        entry.set_title(title)
        
        #submit to server 
        try:
            check_submission = client.upload_to_submission_server(entry, server)
        except:
            print('Failed to submit post to server.')
            ##need to return to somewhere for errors.

        return render_template('viewer.html', link=url, connected = client.isConnected, time = time.ctime())



@app.route('/server_connect/')
def connect_to_post_server():
    client.connect_post_server()
    return render_template('index.html', connected = client.isConnected, time = time.ctime())

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_file(file):
    file = file
    link = ''
    upload = ''

    if file.filename == '':
        return None

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
                if os.path.exists('./static/' + secure_filename(file.filename)):
                    os.remove('./static/' + secure_filename(file.filename))
                return 0

    
    
    if os.path.exists('./static/' + secure_filename(file.filename)):
        os.remove('./static/' + secure_filename(file.filename))

    return upload, link



def main():
    app.run()


if __name__ == "__main__":
    main()