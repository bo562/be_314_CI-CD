"""
py class for professional data structure
"""
from dataclasses import dataclass
from util.database import Database as db, DatabaseLookups as dl
@dataclass
class Professional:
    professional_id: int
    subscription_id: int = None
    def create_professional(self,user_id: int):
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
        query_data = 'PMembership'
        temp_subscription_id = database.database_query(query, query_data)
        if temp_subscription_id is None:
            return "Membership type doesnt exist"
        self.subscription_id = temp_subscription_id
        query = ("INSERT INTO project.professional "
                 "(subscription_id, user_id) "
                 "VALUES (%d, %d)")
        query_data = (self.subscription_id, user_id)
        database.database_query(query, query_data)
        query = "SELECT professional_id FROM project.professional WHERE user_id=%d"
        query_data = (user_id)

        tprofessional_id = database.database_query(query, query_data)
        if tprofessional_id is None:
            return "professional creation failed"
        self.professional_id = tprofessional_id
        database.database_disconnect()

    def update_professional(self, user_id: int):
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
        query_data = 'PMembership'
        temp_subscription_id = database.database_query(query, query_data)
        if temp_subscription_id is None:
            return "Membership type doesnt exist"
        self.subscription_id = temp_subscription_id
        query = ("UPDATE project.professional "
                 "SET subscription_id = %d"
                 "WHERE user_id = %d")
        query_data = (self.subscription_id, user_id)
        database.database_query(query, query_data)
        query = "SELECT professional_id FROM project.professional WHERE user_id=%d"
        query_data = (user_id)

        tprofessional_id = database.database_query(query, query_data)
        if tprofessional_id is None:
            return "professional creation failed"
        self.professional_id = tprofessional_id
        database.database_disconnect()
