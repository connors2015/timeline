import ipfshttpclient
import requests
import webbrowser
import socket
from user import *
from entry import Entry
from time_enums import TimeBlockCategories
import pickle
import random
import time
from time_block import TimeBlock
import os
import sys



IP='13.82.102.90'
#IP='127.0.0.1'
SEPARATOR = "<SEPARATOR>"

class Client:    

    isConnected = False

    def __init__(self):
        #self.client = ipfshttpclient.connect(addr='/ip4/'+IP+'/tcp/8080', session=True)
        self.isConnected = True
        self.addr='http://13.82.102.90:8080/ipfs/'

    
    def upload_to_ipfs(self, fileName):
        print(fileName, 'sadasfafasfasdasda')
        fileName = '{}'.format(fileName)
        file_location = { 'file': open(fileName, 'rb')}
        file = open("sample.txt", 'w')  
    
        # Overwrite the file  
        file.write(" All content has been overwritten !") 
        file.close()

        file_location = { 'file': open("sample.txt", 'rb')}

        r = requests.post(url=addr, files=file_location)
        print(r.headers)
        #client = ipfshttpclient.connect(addr='/ip4/'+IP+'/tcp/8080')
        #try:            
        #    res = self.client.add('./static/'+fileName)['Hash']
        #except:
        #    print('IPFS Daemon not available.')
        return r.headers['ipfs-hash']


    def download_from_ipfs(self, res):
        hashed_res = '{}'.format(res)
        res = self.client.get(hashed_res)
        open_string = 'https://'+IP+':443/ipfs/{}'.format(hashed_res)
        webbrowser.open(open_string, new=0)

    def view_on_ipfs(self, res):
        hashed_res = '{}'.format(res)
        res = self.client.get(hashed_res)
        open_string = 'https://'+IP+':443/ipfs/{}'.format(hashed_res)
        webbrowser.open(open_string, new=2)

    def view_on_web_client(self, res):
        #hashed_res = '{}'.format(res)
        #res = self.client.get(hashed_res)
        open_string = 'https://'+IP+':443/ipfs/{}'.format(res)
        return open_string
        #webbrowser.open(open_string, new=2)

    def connect_to_ipfs(self):
        return 1

    def get_address(self):
        return self.addr

    def disconnect_from_ipfs(self):
        self.client.close()
        self.isConnected = False
        return True

    def upload_to_submission_server(self, entry, server):
        #user = user
        entry = entry
        host = IP #switch to server eventually
        #hashed_res = '{}'.format(entry.get_ipfs_id)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # get local machine name
        #host = socket.gethostname()
        port = 58444

        # connection to hostname on the port.
        s.connect((host, port))

        # Receive no more than 1024 bytes
        # tm = s.recv(1024)

        #entry = Entry(random.randint(0, 8), 'www.reddit.com/{}'.format(random.randint(0,3000000)))
        #entry.set_ipfs_id(hashed_res)
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

        print("Sent submission\t{}".format(entry.get_time()))
        ipfs_servers = []
        ipfs_links_to_blocks = []
        return 1

    def get_posts(self, num_blocks):
        
        host = IP 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 58443

        # connection to hostname on the port.
        s.connect((host, port))

        # Receive no more than 1024 bytes
        # tm = s.recv(1024)

        
        entry_bytes = pickle.dumps(num_blocks)
        s.sendall(entry_bytes)

        #s.close()

        data = s.recv(1024)        

        file_list = pickle.loads(data)
        new_file_list = []

        for items in file_list:
            new_file_list.append(items.decode())
        
        print(file_list)
        print(new_file_list)

        print(len(new_file_list))

        for items in new_file_list:
            filename, filesize = items.split(SEPARATOR)
            print(filesize)
            filename = "./static/"+filename
            with open(filename, 'wb') as file:
                bytes_read = s.recv(5000)
                file.write(bytes_read)
                print('size of bytes read:', sys.getsizeof(bytes_read))
                #if not bytes_read:
                #    break
                #bytes_read = pickle.loads(bytes_read)
                #file.write(bytes_read)

            print('wrote file')
            s.send(b'1')

        timeblocks = []

        for items in new_file_list:
            filename, filesize = items.split(SEPARATOR)
            filename = "./static/"+filename
            print(filename)
            print('file size:', os.path.getsize(filename))
            with open(filename, 'rb') as file:            
                timeblock = pickle.loads(file.read())
            timeblocks.append(timeblock)
            #file.close()

        entries = []

        print('number of timeblocks:', len(timeblocks))

        for items in timeblocks:
            new_list = items.get_entries()
            print(items.get_entries())
            for entry in new_list:
                entries.append(entry)

        for items in entries:
            print(items.get_ipfs_id())

        return entries

    def connect_comment_server(self):
        return 1

def main():

    #app.run()

    #new_user = User()

    client = Client()    
    #print('Uploading.')
    #res = client.upload_to_ipfs('file.txt')
    #print('Finished Uploading.')
    #print('Downloading.')
    #client.view_on_ipfs(res)
    #client.disconnect_from_ipfs()
    #while True:
    #    entry = Entry(TimeBlockCategories.MISC, 'reddit.com')
    #    client.upload_to_submission_server(entry, '1')
    #    time.sleep(random.randint(0,10))
    #client.view_on_ipfs(res)
    #client.disconnect_from_ipfs()

if __name__ == "__main__":
    main()