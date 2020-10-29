import ipfshttpclient
import requests
import webbrowser


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

    def upload_to_submission_server(self):
        return 1

    def connect_submission_server(self, server):

        ipfs_servers = []
        ipfs_links_to_blocks = []

        return 1

    def connect_comment_server(self):
        return 1

def main():

    client = Client()
    print('Uploading.')
    res = client.upload_to_ipfs('lightning.mp4')
    print('Finished Uploading.')
    print('Downloading.')
    client.view_on_ipfs(res)
    client.disconnect_from_ipfs()



if __name__ == "__main__":
    main()