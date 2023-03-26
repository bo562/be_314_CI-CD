from mysql.connector.errors import Error
from mysql.connector import errorcode, MySQLConnection, connect
import json


class Database(MySQLConnection):
    def __init__(self, host, database, user, password):
        super().__init__(user=user, password=password, host=host, database=database)
        self.status = None

    def __del__(self):
        self.Database_Disconnect()

    @staticmethod
    def Database_Handler():
        try:
            # open file and parse json
            fl = '{"server":"csit314-gp.crjrzvrrbory.us-east-1.rds.amazonaws.com","port":3306,"username":"user_lambda",' \
                 '"database":"Project","password":"JRwp~]JfYs2gY*/"} '
            mysql_info = json.loads(fl)
        except Exception as e:
            raise e

        try:
            # attempt database connection
            database = Database(mysql_info['server'], mysql_info['database'],
                                mysql_info['username'], mysql_info['password'])

        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                database.status = "ACCESS DENIED"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                database.status = "DATABASE DOES NOT EXIST"
            else:
                database.status = err
        else:
            database.Database_Disconnect()

        return database

    def Database_Connect(self):
        pass

    def Database_Disconnect(self):
        super().close()

    def Database_Select(self, table):
        pass

    def Database_Insert(self, row):
        pass

    def Database_Update(self):
        pass

    def Database_Delete(self):
        pass

    def Database_Query(self, query):
        pass



