import ipfshttpclient
import webbrowser
import socket
import time
from ntp_time import ntp_time
from entry import Entry
import pickle
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import os
import uuid

class Server:

    def __init__(self):
        #client = ipfshttpclient.connect(addr='/ip4/20.51.191.32/tcp/5001')
        self.entry_buffer = []


    def listen_for_clients(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''
        port = 58444

        # bind to the port
        serversocket.bind((host, port))

        # queue up to 5 requests
        serversocket.listen(5)

        #block_start_time = ntp_time()
        block_start_time = time.time()


        block_number = 0

        while True:
            # establish a connection
            clientsocket, addr = serversocket.accept()

            print("Got a connection from %s" % str(addr))


            print('')
            data = clientsocket.recv(1024)
            #print('data=%s', (data))

            try:
                entry = pickle.loads(data)
            except:
                continue

            print('{}\t\t{}\n{}\t{}'.format(entry.get_time(), entry.get_url(), entry.get_category(), entry.get_ipfs_id()))
            self.entry_buffer.append(entry)

            print('')

         

            if time.time() >= (block_start_time + 60):
                block_start_time = int(time.time())

                fileName = './blocks/{}_{}'.format(block_start_time, block_number)
                file = open(fileName, 'wb')
                pickle.dump(self.entry_buffer, file)
                file.close()

                print('*****************************************')
                print('Timeblock #{} written at {}'.format(block_number, time.ctime(block_start_time)))
                print('*****************************************')

                self.entry_buffer.clear()
                block_number = block_number + 1

          

            #currentTime = time.ctime(time.time()) + "\r\n"
            #clientsocket.send(currentTime.encode('ascii'))
            clientsocket.close()


def main():

    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    print(connect_str)
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = "quickstart" + str(uuid.uuid4())
    container_client = blob_service_client.create_container(container_name)

    local_path = "./data"
    local_file_name = "quickstart" + str(uuid.uuid4()) + ".txt"
    upload_file_path = os.path.join(local_path, local_file_name)

    file = open(upload_file_path, 'w')
    file.write("Hello, World!")
    file.close()

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)


    server = Server()
    server.listen_for_clients()


if __name__ == "__main__":
    main()
