from enum import Enum

class TimeBlockCategories(Enum):
    GENERAL = 0
    SPORTS = 1
    POLITICS = 2
    TECH = 3
    BUSINESS = 4
    MUSIC = 5
    LOCAL = 6
    EVENT = 7
    MISC = 8

class UserAnonLvl(Enum):
    Anonymous = 0
    Anonymous_User = 1
    Verified_Level_2 = 3
    Verified_Level_3 = 4
    Verified_Level_1 = 2
    Business = 5
    Gov = 6
    Event = 7   
