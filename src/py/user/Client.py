"""
py class for client data structure
"""
from dataclasses import dataclass
from mysql.connector import errors
from util.database.Database import Database
from util.database.DatabaseStatus import DatabaseStatus
from util.database.DatabaseLookups import DatabaseLookups


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
        database.clear()
        database.insert(self, 'client', ('client_id',))

        try:
            self.client_id = database.run()
            database.commit()
        except errors.IntegrityError as ie:  # in case that user already exists
            if ie.errno == 1452:  # cannot solve gracefully
                raise ie

            # otherwise integrity violation due to existing value
            database.clear()
            database.select(('client_id',), 'client')
            database.where('user_id = %s', self.user_id)
            self.client_id = database.run()

        # clear database tool
        database.clear()

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
        database.clear()
        database.update(self, 'client', ('client_id',))
        database.where('user_id = %s', self.user_id)

        try:  # attempt to return
            self.client_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:
            raise ie

        # clear database tool
        database.clear()

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

    def get_membership_type(self):
        try:
            database = Database.database_handler(DatabaseLookups.user.value)  # create database to connect to
            database.database_connect()  # connect to database
        except Exception as e:
            print("Database Connection Error")
        query = "SELECT subscription_type FROM project.subscription WHERE subscription_id=%d"
        query_data = (self.subscription_id,)
        return database.database_query(query, query_data)
        database.database_disconnect()

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
