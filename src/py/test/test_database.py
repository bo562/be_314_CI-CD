import unittest
from mysql.connector import errors
from util.database.Database import Database
from util.database.DatabaseStatus import DatabaseStatus
from util.database.DatabaseLookups import DatabaseLookups
from user.User import User

secret_name = '314-db-lambda-user'


class TestDatabase(unittest.TestCase):
    def test_simple_select(self):
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()

        # select from specific table
        database.select(('user.user_id', 'first_name', 'last_name'), 'user')

        # review query
        print(database.review_query())

        # get results from query
        results = database.run()

        print(results)

    def test_where_select(self):
        database = Database.database_handler(DatabaseLookups.User)

        # select from specific table
        database.select(('user_id',), 'user')
        database.where("user_id = %s ", 1)

        # review query
        print(database.review_query())

        # get results from query
        results = database.run()

        print(results)

    def test_inner_select(self):
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()

        # select from specific table
        database.select('user.user_id, client.client_id', 'user')
        database.inner_join('client', 'user.user_id', 'client.user_id')

        # review query
        print(database.review_query())

        # get results from query
        results = database.run()

        print(results)

    def test_insert(self):
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()

        # create test object
        usr = User(first_name='Jason', last_name='Bourne', email_address='jbourne@outlook.com',
                   mobile='88888888', password='password')

        # select from specific table
        database.insert(usr, 'user')

        # review query
        print(database.review_query())

        # get results from query
        results = None
        try:
            results = database.run()
        except errors.IntegrityError as ie:
            print("Functioning Correctly")
        except Exception as e:
            raise e

        print(results)

    def test_update(self):
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()

        # create test object
        usr = User(user_id=8, mobile='99999999', password='password1')

        # select from specific table
        database.update(usr, 'user')
        database.where('user_id = %s', usr.user_id)

        # review query
        print(database.review_query())

        # get results from query
        results = None
        try:
            results = database.run()
        except errors.IntegrityError as ie:
            print("Functioning Correctly")
        except Exception as e:
            raise e

        print(results)

    def test_delete(self):
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()

        # create test object
        usr = User(user_id=8)

        # select from specific table
        database.delete('user')
        database.where('user_id = %s', usr.user_id)

        # review query
        print(database.review_query())

        # get results from query
        results = None
        try:
            results = database.run()
        except errors.IntegrityError as ie:
            print("Functioning Correctly")
        except Exception as e:
            raise e

        print(results)

    def test_query(self):
        # set up database connection and query
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()

        query = "SELECT user.user_id, client.client_id FROM user " \
                "INNER JOIN client ON user.user_id = client.user_id " \
                "WHERE user.user_id = %s"
        args = ('1',)

        results = database.query(query, args)

        print(results)

    def test_temp(self):
        # connect to database
        database = Database.database_handler(DatabaseLookups.User)

        # create database query
        database.clear()
        database.select(('service_id', 'service_name', 'cost', 'retired'), 'service')
        database.where('service_name = %s', 'Tree')

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main(warnings='ignore')
