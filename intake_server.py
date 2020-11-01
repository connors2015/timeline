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
from time_block import TimeBlock

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

        first_block = True
        old_block = TimeBlock(1)

        while True:
            if first_block == True:
                time_block = old_block
                first_block = False
            else:
                time_block = TimeBlock(old_block.get_block_hash)

            clientsocket, addr = serversocket.accept() 
            print("Got a connection from %s" % str(addr))
            print('')
            data = clientsocket.recv(1024)
            #print('data=%s', (data))

            try:
                entry = pickle.loads(data)
            except:
                entry = Entry(0)
                break

            print('{}\n{}\t\t{}\n{}\t{}'.format(entry.get_title(), entry.get_time(), entry.get_url(), entry.get_category(), entry.get_ipfs_id()))
            self.entry_buffer.append(entry)

            print('')


            entry = Entry("MISC", "www.reddit.com")

            time_block.add_new_entry(entry)

            if (block_start_time + 60) < time.time():

                block_start_time = int(time.time())

                fileName = './blocks/{}_{}.blk'.format(block_start_time, block_number)
                upload_filename = '{}_{}.blk'.format(block_start_time, block_number)
                file = open(fileName, 'wb')
                pickle.dump(time_block, file)
                file.close()

                connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
                blob_service_client = BlobServiceClient.from_connection_string(connect_str)
                container_client = blob_service_client.get_container_client("timeline-blocks")
                blob_client = container_client.get_blob_client(blob=upload_filename)

                with open(fileName, "rb") as data:
                    blob_client.upload_blob(data, blob_type="BlockBlob")

                print('*****************************************')
                print('Timeblock #{} written at {}'.format(block_number, time.ctime(block_start_time)))
                print('*****************************************')

               
                os.remove(fileName)
               

                self.entry_buffer.clear()
                block_number = block_number + 1

                old_block = time_block

          

            #currentTime = time.ctime(time.time()) + "\r\n"
            #clientsocket.send(currentTime.encode('ascii'))
            clientsocket.close()


def main():


    server = Server()
    server.listen_for_clients()


if __name__ == "__main__":
    main()
