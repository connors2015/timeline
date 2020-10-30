from flask import Flask
from flask import render_template
from client import Client

app = Flask(__name__)

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

def main():
    app.run()


if __name__ == "__main__":
    main()