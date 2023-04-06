"""
py class for credit card data structure
"""
from dataclasses import dataclass
from datetime import datetime
from util.database import Database as db, DatabaseLookups as dl

@dataclass
class Billing:
    billing_id: int
    name: str = None
    card_number: int = None
    expiry_date: datetime = None
    cvv: str = None
    billing_type: str = None

    def create_billing(self, user_id: int):
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
        query = "SELECT billing_type_id FROM project.billing_type WHERE billing_type_name=%s"
        query_data = (self.billing_type)
        billing_type_id: int = database.database_query(query, query_data)
        query = ("INSERT INTO Project.Billing "
                 "(user_id, card_name, card_number, expiry_date, ccv, billing_type_id) "
                 "VALUES (%d, %s, %s, %s, %s, %d)")
        query_data = (user_id, self.card_number, self.expiry_date.date(), self.cvv, billing_type_id)
        database.database_query(query, query_data)
        query = "SELECT billing_id FROM project.billing WHERE billing_type_id=%d AND user_id = %d"
        query_data = (billing_type_id, self.user_id)

        tbill_id = database.database_query(query, query_data)
        if tbill_id is None:
            return "billing creation failed"
        self.billing_id = tbill_id
        database.database_disconnect()

    def update_billing(self, user_id: int):
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
        query = "SELECT billing_type_id FROM project.billing_type WHERE billing_type_name=%s"
        query_data = self.billing_type
        billing_type_id: int = database.database_query(query, query_data)
        query = ("UPDATE Project.Billing "
                 "SET user_id = %d, card_name = %s, card_number = %s, expiry_date = %s, ccv = %s, billing_type_id = %d "
                 "WHERE user_id =%d AND billing_type_id = %d")
        query_data = (user_id, self.card_number, self.expiry_date.date(), self.cvv, billing_type_id, user_id, billing_type_id)
        database.database_query(query, query_data)
        query = "SELECT billing_id FROM project.billing WHERE billing_type_id=%d AND user_id = %d"
        query_data = (billing_type_id, self.user_id)

        tbill_id = database.database_query(query, query_data)
        if tbill_id is None:
            return "billing creation failed"
        self.billing_id = tbill_id
        database.database_disconnect()
