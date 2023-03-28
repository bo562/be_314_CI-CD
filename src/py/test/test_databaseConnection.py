from util.database import database as d
from util.database.DatabaseStatus import DatabaseStatus

# Setting up a Database Connection
secret_name = "314-db-lambda-user" # aws secret

# create mysql database connection class using handler to set up with much configuration
db = d.Database.database_handler(secret_name)

# test attempt to connnect to database
if db.status is DatabaseStatus.Connected:
    result = db.database_query("SELECT * FROM test_python")
    print(result)

