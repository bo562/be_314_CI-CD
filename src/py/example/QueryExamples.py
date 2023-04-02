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

# create database class and connect to database
database_connection = db.Database.database_handler(secret_name)

# catch database connection error (in reality the exception handling should be better)
try:
    database_connection.database_connect()
except Exception as e:
    print("Database Connection Error")

# simple query on user table
query = "SELECT * FROM User"  # write query, very similar to normal SQL
results = database_connection.database_query(query)  # push query to db and fetch results
print(results)

# queries with search parameters
query = "SELECT * FROM User WHERE user_id = %s "
results = database_connection.database_query(query, tuple("1"))
print(results)

# queries with inner joins parameters
query = "SELECT * FROM User " \
        "INNER JOIN Address ON User.User_id = Address.User_id"
results = database_connection.database_query(query)
print(results)

# queries with inner joins parameters and WHERE clause
query = "SELECT * FROM User " \
        "INNER JOIN Address ON User.User_id = Address.User_id " \
        "WHERE User.User_id = %s"
results = database_connection.database_query(query, tuple("2"))
print(results)

database_connection.database_disconnect()
