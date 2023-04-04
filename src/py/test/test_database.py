import unittest
from util.database import Database as db, DatabaseStatus as ds
from util.database.DatabaseLookups import DatabaseLookups

secret_name = '314-db-lambda-user'


class TestDatabase(unittest.TestCase):
    def ttest_database_connection(self):
        database = db.Database.database_handler(DatabaseLookups.User.value)  # create database to connect to
        database.database_connect()  # connect to database
        self.assertEqual(database.status, ds.DatabaseStatus.Connected)

    def ttest_database_query(self):
        database = db.Database.database_handler(DatabaseLookups.User.value)  # create database to connect to
        database.database_connect()  # connect to database

        # check if connected to database
        if database.status is not ds.DatabaseStatus.Connected:
            raise Exception()

        # run query to database
        query = "SELECT * FROM User WHERE user_id = %s"
        user_id = "1"
        result = database.database_query(query, tuple(user_id))

    def ttest_database_query1(self):
        database = db.Database.database_handler(DatabaseLookups.User.value)  # create database to connect to
        database.database_connect()  # connect to database

        # check if connected to database
        if database.status is not ds.DatabaseStatus.Connected:
            raise Exception()

        # run query to database
        query = "SELECT * FROM User"
        result = database.database_query(query)

    def ttest_database_insert(self):
        database = db.Database.database_handler(DatabaseLookups.User.value)  # create database to connect to
        database.database_connect()  # connect to database

        # check if connected to database
        if database.status is not ds.DatabaseStatus.Connected:
            raise Exception()

        # run query to database
        results = database.database_insert(('first_name', 'last_name', 'email_address', 'mobile', 'password'),
                                 ('Jorge', 'Havel', 'jhavel@gmail.com', '4545454545', 'asdasdasdfff'), 'user')

        print(results)

    def test_database_update(self):
        database = db.Database.database_handler(DatabaseLookups.User.value)  # create database to connect to
        database.database_connect()  # connect to database

        # check if connected to database
        if database.status is not ds.DatabaseStatus.Connected:
            raise Exception()

        database.database_connection.cursor()

        print(results)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main(warnings='ignore')
