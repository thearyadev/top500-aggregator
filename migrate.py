import database
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

db = database.DatabaseAccess("./data/data.db")
# print(len(db.get_all_records("5_8")))
tdb = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=os.getenv("MYSQLPORT"),
)

cursor = tdb.cursor()
cursor.execute("SELECT * FROM season_info")

print(cursor.fetchall())