import time
from time_enums import TimeBlockCategories
from ntp_time import ntp_time


class Entry:

    category = TimeBlockCategories.MISC
    entry_time = time.ctime(ntp_time())
    entry_url = ''
    ipfs_id = ''
    location = ''

    def __init__(self, category, url):
        self.category = TimeBlockCategories(category)
        self.url = url

    def get_url(self):
        return self.url

    def get_time(self):
        return self.entry_time

    def get_ipfs_id(self):
        return self.ipfs_id

    def get_location(self):
        return self.location



class TimeBlock:

    currentTime = time.ctime(ntp_time())
    entries = []


def main():

    block1 = TimeBlock

    # print(time.ctime(ntp_time()).replace("  ", " "))


if __name__ == "__main__":
    main()