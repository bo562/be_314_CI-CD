import unittest
from util.database import Database as db, DatabaseStatus as ds, DatabaseLookups as dl


class TestDatabase(unittest.TestCase):
    def test_database_connection(self):
        database = db.Database.database_handler(dl.DatabaseLookups.User.value)  # create database to connect to
        database.database_connect()  # connect to database
        self.assertEqual(database.status, ds.DatabaseStatus.Connected)

    def test_database_query(self):
        database = db.Database.database_handler(dl.DatabaseLookups.User.value)  # create database to connect to
        database.database_connect()  # connect to database

        # check if connected to database
        if database.status is not ds.DatabaseStatus.Connected:
            raise Exception()

        # run query to database
        query = "SELECT %s, %s, %s FROM User WHERE user_id = %s"
        user_id = "1"
        result = database.database_query(query, tuple(user_id))

    def test_database_query1(self):
        database = db.Database.database_handler(dl.DatabaseLookups.User.value)  # create database to connect to
        database.database_connect()  # connect to database

        # check if connected to database
        if database.status is not ds.DatabaseStatus.Connected:
            raise Exception()

        # run query to database
        query = "SELECT * FROM User"
        result = database.database_query(query)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main(warnings='ignore')
