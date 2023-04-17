"""
py class for client data structure
"""
from dataclasses import dataclass
from mysql.connector import errors
from util.database.Database import Database
from util.database.DatabaseStatus import DatabaseStatus
from util.database.DatabaseLookups import DatabaseLookups
from user.Subscription import Subscription
from util.handling.errors.database.DatabaseObjectAlreadyExists import DatabaseObjectAlreadyExists
from util.handling.errors.database.FailedToCreateDatabaseObject import FailedToCreateDatabaseObject
from util.handling.errors.database.FailedToUpdateDatabaseObject import FailedToUpdateDatabaseObject


@dataclass
class Client:
    client_id: int = None
    user_id: int = None
    subscription_id: int = None

    def create_client(self, user_id: int):
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise errors.InternalError  # change with mysql errors

        # if user_id null set user_id
        if self.user_id is None:
            self.user_id = user_id

        # attempt to create client now
        database.insert(self, 'client', ('client_id',))

        try:
            self.client_id = database.run()
            database.commit()
        except errors.IntegrityError as ie:
            database.rollback()
            query = database.review_query()
            database.clear()
            database.disconnect()

            # if there is an integrity error
            if ie.errno == 1452:  # cannot solve gracefully
                # raise error
                raise DatabaseObjectAlreadyExists(table='user', query=query, database_object=self)

            # some other consistency constraint check
            raise FailedToCreateDatabaseObject(table='user', query=query, database_object=self)

        # clear database tool
        database.clear()
        database.disconnect()

        return self

    def update_client(self, user_id: int):
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise errors.InternalError  # change with mysql errors

        # attempt to create billing object
        if self.user_id is None:
            self.user_id = user_id

        # create query
        database.update(self, 'client', ('client_id',))
        database.where('user_id = %s', self.user_id)

        try:  # attempt to return
            self.client_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:
            database.rollback()
            query = database.review_query()
            database.clear()
            database.disconnect()

            # if there is an integrity error
            if ie.errno == 1452:  # cannot solve gracefully
                # raise error
                raise DatabaseObjectAlreadyExists(table='user', query=query, database_object=self)

            # some other consistency constraint check
            raise FailedToUpdateDatabaseObject(table='user', query=query, database_object=self)

        # clear database tool
        database.clear()
        database.disconnect()

        return self

    def delete_client(self):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()

        database.delete('client')
        database.where('client_id = %s', self.client_id)

        try:
            database.run()
            database.commit()
        except Exception as e:
            return False

        return True

    @staticmethod
    def get_client(user_id: int):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # get user object
        database.clear()
        database.select(('client_id', 'subscription_id', 'user_id'),
                        'client')
        database.where('user_id = %s', user_id)

        # try to get authorisation
        client = None
        try:
            results = database.run()

        except Exception as e:
            raise e

        if len(results) > 0:
            client = Client(client_id=results[0][0], subscription_id=results[0][1], user_id=results[0][2])

        return client

    @staticmethod
    def get_by_client_id(client_id: int):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # get user object
        database.clear()
        database.select(('client_id', 'subscription_id', 'user_id'),
                        'client')
        database.where('client_id = %s', client_id)

        # try to get authorisation
        try:
            results = database.run()

        except Exception as e:
            raise e

        client = None
        if len(results) > 0:
            client = Client(client_id=results[0][0], subscription_id=results[0][1], user_id=results[0][2])

        return client

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Client):
            # take subscription_id and get name
            database = Database.database_handler(DatabaseLookups.User)
            database.clear()
            database.select(('subscription_name',), 'subscription')
            database.where('subscription_id = %s', obj.subscription_id)
            results = database.run()

            subscription_name = results[0][0] if results is not None else None

            remap = {
                "membershipType": subscription_name
            }
            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        # take membership type and return subscription_id

        database = Database.database_handler(DatabaseLookups.User)
        database.clear()
        database.select(('subscription_id',), 'subscription')
        database.where('subscription_name = %s', obj.get('membershipType'))
        results = database.run()
        subscription_id = results[0][0] if results is not None else None

        return Client(client_id=None, subscription_id=subscription_id)
