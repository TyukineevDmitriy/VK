#from bottle import Bottle, route, run, debug, template
from models import *
from db_updater import *
import time
from vk_requests import *

#app = Bottle()
"""def update_database():
    users = []
    for user in User.select(User.id):
        users.append(user.id)"""

print("Enter a number of user to watch his newsticker")
t = time.time()
#kek = VK_requests()
#print(len(kek.get_friends(340181344)))
db_updater = DB_updater()
db_updater.update()
print(time.time() - t)
#number = input()
#number = 56783288
#newsticker = Newsticker(number=number)

'''while True:
    print("Enter a number of sorts:"
          "\n1: by likes"
          "\n2: by reposts"
          "\n3: by comments")
    sort = input()
    if int(sort) == 1:
        newsticker.sort_by_likes()
    elif int(sort) == 2:
        newsticker.sort_by_reposts()
    elif int(sort) == 3:
        newsticker.sort_by_comments()
    print(newsticker.newsticker)
    for n in newsticker.newsticker:
        print(n)'''



"""@route('/')
def todo_list():

    return "kek"

debug(True)
run()"""