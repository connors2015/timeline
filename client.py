import ipfshttpclient
from ntp_time import ntp_time
import requests
import webbrowser
import socket
from user import *
from entry import Entry
from time_enums import TimeBlockCategories
import pickle
import random
import time


class Client:

    def __init__(self):
        self.client = ipfshttpclient.connect(addr='/ip4/20.51.191.32/tcp/5001', session=True)

    def upload_to_ipfs(self, file):
        #client = ipfshttpclient.connect(addr='/ip4/20.51.191.32/tcp/5001')
        res = self.client.add(file)['Hash']
        return res

    def download_from_ipfs(self, res):
        hashed_res = '{}'.format(res)
        res = self.client.get(hashed_res)
        open_string = 'http://20.51.191.32:8080/ipfs/{}'.format(hashed_res)
        webbrowser.open(open_string, new=0)

    def view_on_ipfs(self, res):
        hashed_res = '{}'.format(res)
        #res = self.client.get(hashed_res)
        open_string = 'http://20.51.191.32:8080/ipfs/{}'.format(hashed_res)
        webbrowser.open(open_string, new=2)

    def connect_to_ipfs(self):
        return 1

    def disconnect_from_ipfs(self):
        self.client.close()
        return True

    def upload_to_submission_server(self, hash, server, user):
        user = user
        host = server
        hashed_res = '{}'.format(hash)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # get local machine name
        #host = socket.gethostname()
        port = 9999

        # connection to hostname on the port.
        s.connect((host, port))

        # Receive no more than 1024 bytes
        # tm = s.recv(1024)

        entry = Entry(random.randint(0, 8), 'www.reddit.com/{}'.format(random.randint(0,3000000)))
        entry.set_ipfs_id(hashed_res)
        entry_bytes = pickle.dumps(entry)
        #hashed_entry = bytes(entry)
        #title = 'Flying over NYC in MSF2020'
        #hashed_res = bytes(hashed_res, 'utf-8')
        #hashed_title = bytes(title, 'utf-8')
        #hashed_username = bytes(user.get_username(), 'utf-8')
        s.sendall(entry_bytes)
        #l = file.read(1024)

        #s.send(hashed_username)
        #s.sendall(hashed_title)

        s.close()

        print("Sent submission\t{}".format(time.ctime(ntp_time())))
        ipfs_servers = []
        ipfs_links_to_blocks = []
        return 1

    def connect_submission_server(self):
        return 1

    def connect_comment_server(self):
        return 1

def main():

    new_user = User()

    client = Client()
    #print('Uploading.')
    res = client.upload_to_ipfs('file.txt')
    #print('Finished Uploading.')
    #print('Downloading.')
    #client.view_on_ipfs(res)
    #client.disconnect_from_ipfs()
    while True:
        client.upload_to_submission_server(res, '20.51.191.32', new_user)
        time.sleep(random.randint(0,5))
    #client.view_on_ipfs(res)
    client.disconnect_from_ipfs()



if __name__ == "__main__":
    main()