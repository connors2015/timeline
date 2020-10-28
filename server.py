import ipfshttpclient
import webbrowser



client = ipfshttpclient.connect(addr='/ip4/127.0.0.1/tcp/5001')
res = client.add('lightning.mp4')['Hash']
print(res)

hash = '{}'.format(res)

res = client.get(hash)
open_string = 'http://127.0.0.1:8080/ipfs/{}'.format(hash)
webbrowser.open(open_string, new=2)
