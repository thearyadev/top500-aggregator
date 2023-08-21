import database
import mysql.connector

db = database.DatabaseAccess("./data/data.db")
print(len(db.get_all_records("5_8")))