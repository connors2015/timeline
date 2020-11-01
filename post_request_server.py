import requests
import pickle
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import os
from time_block import TimeBlock
from entry import Entry
import socket

SEPARATOR = "<SEPARATOR>"

class PostServer:

    def __init__(self):
        self.amount_of_blocks = 1

    def listen_for_requests(self):

        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''
        port = 58443

        # bind to the port
        serversocket.bind((host, port))

        # queue up to 5 requests
        serversocket.listen(5)

        while True:

            clientsocket, addr = serversocket.accept() 
            #print("Got a connection from %s" % str(addr))
            print('')

            data = clientsocket.recv(1024)

            #print('data=%s', (data))

            self.amount_of_blocks = pickle.loads(data)

            file_list = self.retrieve_blocks(self.amount_of_blocks)

            sending_file_list = []

            for items in file_list:
                filesize = os.path.getsize("./static/"+items)
                sending_file_list.append((f"{items}{SEPARATOR}{filesize}".encode()))
            
            clientsocket.sendall(pickle.dumps(sending_file_list))

            print(file_list)

            counter = 0

            for items in file_list:
                print(counter)
                filename = "./static/"+items
                print(filename)
                print(type(filename))
                file = open(filename, 'r')
                print(type(file))
                #with open(filename, 'r') as data:
                #    print(type(data))
                #data = pickle.dumps(file)
                clientsocket.send(data)
                clientsocket.recv(1)
                counter = counter + 1
            
            clientsocket.close()


    def retrieve_blocks(self, amount_of_blocks):

        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_client = blob_service_client.get_container_client("timeline-blocks")

        #List of blobs in container
        blob_list = container_client.list_blobs()

        file_list = []

        for items in blob_list:
            blob_client = container_client.get_blob_client(blob=items)

            file_list.append(items.name)

            with open("./static/"+items.name, "wb") as my_blob:
                blob_data = blob_client.download_blob()
                blob_data.readinto(my_blob)   

        return file_list     



def main():

    post_server = PostServer()
    post_server.listen_for_requests()

if __name__ == "__main__":
    main()