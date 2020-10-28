import time
from time_enums import TimeBlockCategories
from ntp_time import ntp_time

#print(time.ctime(ntp_time()).replace("  ", " "))

class TimeBlock:

    currentTime = time.ctime(ntp_time())
    category = TimeBlockCategories.MISC





def main():

    block1 = TimeBlock

    print(TimeBlock.category.value)


if __name__ == "__main__":
    main()