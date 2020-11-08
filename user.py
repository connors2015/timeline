import random
from time_enums import UserAnonLvl

MAX_LIMIT = 78


class User:   

    def __init__(self):
        random_string = ''
        for _ in range(32):
            random_integer = random.randint(22, MAX_LIMIT)
            # Keep appending random characters using chr(x)
            random_string += (chr(random_integer)) 
            print(random_string)
        self.username = random_string
        self.anon_level = User

    def get_username(self):
        return self.username


def main():
    user = User()

    print(user.get_username())


if __name__ == "__main__":
    main()