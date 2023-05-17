import os
import create_database as db_creator
from database import session

from database import DATABASE_NAME
import server

db_is_created = os.path.exists(DATABASE_NAME)
if not db_is_created:
    db_creator.create_database(load_fake_data=True)  # add load_fake_data=True if fake data needed

print("[STARTING] server is starting...")
server.start()
