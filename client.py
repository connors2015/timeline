import ipfshttpclient
import requests
import webbrowser


class Client:

    def __init__(self):
        self.client = ipfshttpclient.connect(addr='/ip4/127.0.0.1/tcp/5001', session=True)

    def upload_to_ipfs(self, file):
        res = self.client.add('file.txt')['Hash']
        print(res)
        return res

    def download_from_ipfs(self, hash):
        res = self.client.get(hash)
        open_string = 'http://127.0.0.1:8080/ipfs/{}'.format(hash)
        webbrowser.open(open_string, new=2)

    def connect_to_ipfs(self):
        return 1

    def disconnect_from_ipfs(self):
        self.client.close()
        return True

    def upload_to_submission_server(self):
        return 1

    def connect_submission_server(self, server):

        ipfs_servers = []
        ipfs_links_to_blocks = []

        return 1

    def connect_comment_server(self):
        return 1