'''
py giving examples on how to set up database connection
'''

from util.database import Database as db
from util.database import DatabaseStatus as ds

# Setting up Database Connection
'''
currently there is only one set of credentials, but in time we will have multiple sets of credentials
for different lambdas so this will change in future
'''

secret_name = '314-db-lambda-user'  # current user lambda

# create database class to handle connection and queries pass secret_name for credentials
database_connection = db.Database.database_handler(secret_name)

# connect to database and ensure connection is valid
database_connection.database_connect()

if database_connection.status is not ds.DatabaseStatus.Connected:
    print("Database not connected")
else:
    print("Database is connected!")

# Disconnecting from a database
database_connection.database_disconnect()

if database_connection.status is not ds.DatabaseStatus.Connected:
    print("Database not connected")
else:
    print("Database is connected!")