import time
from time_enums import TimeBlockCategories
from ntp_time import ntp_time
import urllib.request, urllib.error, urllib.parse
import webbrowser
import hashlib


class Entry:

    category = TimeBlockCategories.MISC
    entry_ctime = ntp_time()
    entry_time = time.ctime(entry_ctime)
    entry_url = ''
    entry_url_hash = ''
    entry_hash = ''
    ipfs_id = ''
    location = ''
    user_id = ''

    def __init__(self, category, url):
        url_hasher = hashlib.sha3_256()
        entry_hasher = hashlib.sha3_256()
        binary_url = bytes(url, 'utf-8')
        url_hasher.update(binary_url)

        self.category = TimeBlockCategories(category)
        self.entry_url = url
        self.entry_url_hash = url_hasher.hexdigest()

        hash_setup = '{}{}'.format(url, self.entry_ctime, self.user_id)
        hash_setup = bytes(hash_setup, 'utf-8')
        entry_hasher.update(hash_setup)

        self.entry_hash = entry_hasher.hexdigest()
        #self.store_url_snapshot(url)

    def get_url(self):
        return self.entry_url

    def get_category(self):
        return self.category

    def get_time(self):
        return self.entry_time

    def get_ctime(self):
        return self.entry_ctime

    def get_ipfs_id(self):
        return self.ipfs_id

    def get_entry_hash(self):
        return self.entry_hash

    def get_entry_url_hash(self):
        return self.entry_url_hash

    def get_location(self):
        return self.location

    def open_url_snapshot(self):
        webbrowser.open('{}'.format(self.entry_url), new=2)

    def set_ipfs_id(self, hash):
        self.ipfs_id = hash

    def store_url_snapshot(self, url):
        url = self.entry_url

        response = urllib.request.urlopen(url)
        webContent = response.read()

        f = open('{}'.format(url), 'wb')
        f.write(webContent)
        f.close