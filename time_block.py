import time
from time_enums import TimeBlockCategories
from ntp_time import ntp_time
from entry import Entry
import struct
import hashlib


class TimeBlock:

    block_hasher = hashlib.sha3_256()
    block_ctime = ntp_time()
    block_time = time.ctime(block_ctime)
    previous_ipfs_hash = ''
    entries = []

    def __init__(self, previous_ipfs_hash):
        self.previous_ipfs_hash = previous_ipfs_hash

    def add_new_entry(self, entry):
        if isinstance(entry, Entry):
            self.entries.append(entry)
        else:
            print('Invalid Entry.')

    def get_block_hash(self):

        entry_bytes = b''

        for entries in self.entries:
            entry_bytes = entry_bytes + bytes(entries.get_entry_hash(), 'utf-8')

        hash_setup = '{}{}'.format(self.block_ctime, self.previous_ipfs_hash)
        hash_setup = bytes(hash_setup, 'utf-8')
        hash_setup = entry_bytes + hash_setup
        self.block_hasher.update(hash_setup)

        return self.block_hasher.hexdigest()

    def get_block_time(self):
        return self.block_time

    def get_block_ctime(self):
        return self.block_ctime

    def print(self):
        for entries in self.entries:
            print('{}\t{}\t{}\t{}'.format(entries.get_time(), entries.get_category(), entries.get_url(), entries.get_entry_url_hash()))





def main():



    block1 = TimeBlock('')

    entry1 = Entry(0, 'https://www.cnn.com')
    entry2 = Entry(3, 'https://www.reddit.com')
    entry3 = Entry(6, 'https://www.facebook.com')


    block1.add_new_entry(entry1)
    block1.add_new_entry(entry2)
    block1.add_new_entry(entry3)

    block1.print()
    print('Block Hash:', block1.get_block_hash())



if __name__ == "__main__":
    main()