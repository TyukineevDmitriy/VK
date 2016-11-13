from models import orm_models
from db_updater import *
import time

t = time.time()
db_updater = DB_updater()
db_updater.update_users()
print(time.time() - t)


