import ipfshttpclient
import webbrowser

class Server:

    def __init__(self):
        client = ipfshttpclient.connect(addr='/ip4/127.0.0.1/tcp/5001')
        client.close()
        open_string = 'http://20.51.191.32:8080/ipfs/{}'.format(hash)
        webbrowser.open(open_string, new=2)


def main():

    server = Server()


if __name__ == "__main__":
    main()
