from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import render_template
from client import Client
from time_enums import TimeBlockCategories
from entry import Entry
import os
import time
import requests

UPLOAD_FOLDER = '/static/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'flac'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#for the love of god please setup ssh keys.
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


client = Client()

@app.route('/')
def index():
    posts = get_posts(2)
    #entry = Entry(TimeBlockCategories.MISC, 'www.reddit.com') #use when there are no blocks
    #posts = [entry,entry,entry] #use when there are no blocks
    return render_template('index.html', time = time.ctime(), connected = client.isConnected, posts = posts)

@app.route('/make_new_post')
def make_new_post():
    return render_template('make_new_post.html', time=time.ctime(), connected= client.isConnected)

@app.route('/new_post', methods=['POST', 'GET'])
def upload_new_post():

    server = '1.1.1.1'
    title  = request.form['title']
    url = request.form['url']
    print(title, url)
    print('made it in.***********************')
    print(request.form['categories'])

    post_category = TimeBlockCategories(int((request.form['categories'])))

    entry = Entry(post_category, url)
    #run upload file and retrieve IPFS hash and IPFS web hash
    file = request.files['file']
    if file.filename != '':
        file_hash, web_link = upload_file(request.files['file'])
        entry.set_ipfs_id(file_hash) 
        entry.set_title(title)
        entry.set_comments(request.form['comment'])

        try:
            check_submission = client.upload_to_submission_server(entry, server)
        except:
            print('Failed to submit post to server.')
            ##need to return to somewhere for errors.
        
        #if os.path.exists('./static/' + secure_filename(file.filename)):
        #    os.remove('./static/' + secure_filename(file.filename))

        return render_template('viewer.html', link=web_link, connected = client.isConnected, time = time.ctime())
    else:
        entry.set_title(title)
        entry.set_comments(request.form['comment'])
        
        #submit to server 
        try:
            check_submission = client.upload_to_submission_server(entry, server)
        except:
            print('Failed to submit post to server.')
            ##need to return to somewhere for errors.

    

        return render_template('viewer.html', link=url, connected = client.isConnected, time = time.ctime())



@app.route('/server_connect/<string:server>')
def connect_to_post_server(server):
    client.connect_post_server(server)
    return render_template('index.html', connected = client.isConnected, time = time.ctime())

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_file(file):
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
                file1 = open('./static/' + secure_filename(file.filename), 'rb')
                req = requests.post(url=client.get_address(), data=file1)
                file_hash = req.headers['ipfs-hash']
                print(file_hash)
                while file_hash == None:
                    time.sleep(1)
                print('uploaded')
                full_url = client.view_on_web_client(file_hash)
                print(full_url)
       
            except:
                print('error uploading')
                string = 'error uploading to IPFS'
                if os.path.exists('./static/' + secure_filename(file.filename)):
                    os.remove('./static/' + secure_filename(file.filename))
                return 0

    
    
    #if os.path.exists('./static/' + secure_filename(file.filename)):
    #    file.close()
    #    os.remove('./static/' + secure_filename(file.filename))

    return file_hash, full_url

def get_posts(num_blocks):
    posts = client.get_posts(num_blocks)
    return posts

def main():
    app.run()


if __name__ == "__main__":
    main()