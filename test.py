import ipfshttpclient
import requests
import webbrowser

addr= 'http://13.82.102.90:8080/ipfs/'

#client = ipfshttpclient.Client()

#client = ipfshttpclient.connect(addr='/ip4/'+IP+'/tcp/8080', session=True)


# open the file using open() function 
#file = open("sample.txt", 'w')  
    
# Overwrite the file  
#file.write(" All content has been overwritten !") 
#file.close()

file_location = { 'file': open("./static/lightning.mp4", 'r')}
file = open('./static/lightning.mp4', 'rb')

r = requests.post(url=addr, data=file)
#print(file.name)
#r = requests.put(url=IP+r.headers['ipfs-hash'], params=file.name)

print(r)
print(r.headers)
print(r.links)
print(r.text)
print('')
print(r.content)

print('added file')