"""
py class for client data structure
"""
from dataclasses import dataclass
from util.database.Database import Database
from util.database.DatabaseStatus import DatabaseStatus
from util.database.DatabaseLookups import DatabaseLookups


@dataclass
class Client:
    client_id: int = None
    user_id: int = None
    subscription_id: int = None

    def create_client(self, user_id: int, membership_type):
        try:
            database = Database.database_handler(DatabaseLookups.user.value)  # create database to connect to
            database.database_connect()  # connect to database
            query = "SELECT user_id FROM project.user WHERE user_id=%d"
            query_data = (user_id)
            validationcheck = database.database_query(query, query_data)
            if not isinstance(validationcheck, int) or validationcheck < 0:
                return "invalid id"
        except Exception as e:
            print("Database Connection Error")
        query = "SELECT subscription_id FROM project.subscription WHERE subscription_type=%s"
        query_data = (membership_type)
        tsub_id = database.database_query(query, query_data)
        if tsub_id is None:
            return "Membership type doesnt exist"
        self.subscription_id = tsub_id
        query = ("INSERT INTO project.clients "
                 "(subscription_id, user_id) "
                 "VALUES (%d, %d)")
        query_data = (self.subscription_id, user_id)
        database.database_query(query, query_data)
        query = "SELECT client_id FROM project.client WHERE user_id=%d"
        query_data = (user_id)

        tclient_id = database.database_query(query, query_data)
        if tclient_id is None:
            return "billing creation failed"
        self.clint_id = tclient_id
        database.database_disconnect()

    def update_client(self, user_id: int, membership_type):
        try:
            database = Database.database_handler(DatabaseLookups.user.value)  # create database to connect to
            database.database_connect()  # connect to database
            query = "SELECT user_id FROM project.user WHERE user_id=%d"
            query_data = (user_id)
            validationcheck = database.database_query(query, query_data)
            if not isinstance(validationcheck, int) or validationcheck < 0:
                return "invalid id"
        except Exception as e:
            print("Database Connection Error")
        query = "SELECT subscription_id FROM project.subscription WHERE subscription_type=%s"
        query_data = (membership_type)
        tsub_id = database.database_query(query, query_data)
        if tsub_id is None:
            return "Membership type doesnt exist"
        self.subscription_id = tsub_id
        query = ("UPDATE project.clients "
                 "SET subscription_id = %d "
                 "WHERE user_id = %d")
        query_data = (self.subscription_id, user_id)
        database.database_query(query, query_data)
        query = "SELECT client_id FROM project.client WHERE user_id=%d"
        query_data = (user_id)

        tclient_id = database.database_query(query, query_data)
        if tclient_id is None:
            return "billing creation failed"
        self.clint_id = tclient_id
        database.database_disconnect()

    def get_membership_type(self):
        try:
            database = Database.database_handler(DatabaseLookups.user.value)  # create database to connect to
            database.database_connect()  # connect to database
        except Exception as e:
            print("Database Connection Error")
        query = "SELECT subscription_type FROM project.subscription WHERE subscription_id=%d"
        query_data = (self.subscription_id)
        return database.database_query(query, query_data)
        database.database_disconnect()
        
    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Client):
            # take subscription_id and get name
            database = Database.database_handler(DatabaseLookups.User)
            database.select('subscription_name', 'subscription')
            database.where('subscription_id = %s', obj.subscription_id)
            subscription_name = database.run()

            remap = {
                "membershipType": subscription_name[0][0]
            }
            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        # take membership type and return subscription_id
        database = Database.database_handler(DatabaseLookups.User)
        database.select('subscription_id', 'subscription')
        database.where('subscription_name = %s', obj.get('membershipType'))
        subscription_id = database.run()

        return Client(client_id=-1, subscription_id=subscription_id[0][0])
