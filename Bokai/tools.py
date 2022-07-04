import os
import dotenv 
import random
from random import randint

def get_guild():
    return [os.getenv('GUILD_ID')]


def random_number():
    lst = []
    while len(lst) < 4:
        lst.append(str(randint(1,9)))
        if len(lst) > 1:
            x = 0
            while x < len(lst)-1:
                if lst[x] == lst[len(lst)-1]:
                    del lst[len(lst)-1]
                else:
                    x += 1
    # print(lst)
    return lst



def workingdir(dir):

    return os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), dir))





# print(random.randint(1000,9999))