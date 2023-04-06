"""
py class for client data structure
"""
from dataclasses import dataclass
from util.database import Database as db, DatabaseLookups as dl

@dataclass
class Client:
    client_id: int
    subscription_id: int = None

    def create_client(self, user_id: int, membership_type):
        try:
            database = db.Database.database_handler(dl.DatabaseLookups.user.value)  # create database to connect to
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
            database = db.Database.database_handler(dl.DatabaseLookups.user.value)  # create database to connect to
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

    def get_membershiptype(self):
        try:
            database = db.Database.database_handler(dl.DatabaseLookups.user.value)  # create database to connect to
            database.database_connect()  # connect to database
        except Exception as e:
            print("Database Connection Error")
        query = "SELECT subscription_type FROM project.subscription WHERE subscription_id=%d"
        query_data = (self.subscription_id)
        return database.database_query(query, query_data)
        database.database_disconnect()