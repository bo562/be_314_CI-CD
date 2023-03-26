from util.database import database as d
import mysql.connector
import os

db = d.Database.Database_Handler()
print(db.status)
db.__del__()

#cursor = db.database.cursor()
#result = cursor.execute("SELECT * FROM User")