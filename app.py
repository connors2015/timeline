from flask import Flask
from flask import render_template
from client import Client

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/<string:filename>')
def run_upload(filename):
    #file = open('file.txt', 'r')
    client = Client()
    upload = client.upload_to_ipfs(filename)
    link = client.view_on_web_client(upload)
    return render_template('viewer.html', link = link)

def main():
    app.run()


if __name__ == "__main__":
    main()