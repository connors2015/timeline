import ipfshttpclient
import webbrowser
import socket
import time
from ntp_time import ntp_time
from entry import Entry
import pickle

class Server:

    def __init__(self):
        client = ipfshttpclient.connect(addr='/ip4/20.51.191.32/tcp/5001')

    def listen_for_clients(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''
        port = 9999

        # bind to the port
        serversocket.bind((host, port))

        # queue up to 5 requests
        serversocket.listen(5)

        while True:
            # establish a connection
            clientsocket, addr = serversocket.accept()

            print("Got a connection from %s" % str(addr))
            with open('received_file', 'wb') as file:
                while True:
                    print('receiving data...')
                    data = serversocket.recv(1024)
                    print('data=%s', (data))
                    if not data:
                        break
                    # write data to a file
                    file.write(data)

            entry = pickle.load(file)

            print(entry.get_url())

            #currentTime = time.ctime(time.time()) + "\r\n"
            #clientsocket.send(currentTime.encode('ascii'))
            #clientsocket.close()


def main():

    server = Server()
    server.listen_for_clients()


if __name__ == "__main__":
    main()
