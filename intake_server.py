import ipfshttpclient
import webbrowser
import socket
import time
from ntp_time import ntp_time
from entry import Entry
import pickle

class Server:

    def __init__(self):
        #client = ipfshttpclient.connect(addr='/ip4/20.51.191.32/tcp/5001')
        self.entry_buffer = []

    def listen_for_clients(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''
        port = 9999

        # bind to the port
        serversocket.bind((host, port))

        # queue up to 5 requests
        serversocket.listen(5)

        block_start_time = ntp_time()

        block_number = 0

        while True:
            # establish a connection
            clientsocket, addr = serversocket.accept()

            print("Got a connection from %s" % str(addr))


            print('receiving data...')
            data = clientsocket.recv(1024)
            #print('data=%s', (data))

            try:
                entry = pickle.loads(data)
            except:
                continue

            print('{}\t\t{}\n{}\t{}'.format(entry.get_ctime(), entry.get_url(), entry.get_category(), entry.get_ipfs_id()))
            self.entry_buffer.append(entry)

            print('')
            print(block_start_time, block_start_time+60)
            print('')

            if ntp_time() > (block_start_time + 60):
                block_start_time = ntp_time()

                fileName = './blocks/{}_{}'.format(block_start_time, block_number)
                file = open(fileName, 'wb')
                pickle.dump(self.entry_buffer, file)
                file.close()
                print('Timeblock #{} written at {}'.format(block_number, block_start_time))

                self.entry_buffer.clear()
                block_number = block_number + 1

            #currentTime = time.ctime(time.time()) + "\r\n"
            #clientsocket.send(currentTime.encode('ascii'))
            clientsocket.close()


def main():

    server = Server()
    server.listen_for_clients()


if __name__ == "__main__":
    main()
