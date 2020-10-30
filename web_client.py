from flask import Flask
from flask import render_template
from client import Client

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/')
def run_upload():
    #file = open('file.txt', 'r')
    client = Client()
    upload = client.upload_to_ipfs('file.txt')
    return 'Upload Successfull! {}'.format(upload)

def main():
    app.run()


if __name__ == "__main__":
    main()