"""
py class for credit card data structure
"""
from dataclasses import dataclass
from mysql.connector import errors
from util.database.Database import Database
from util.database.DatabaseStatus import DatabaseStatus
from util.database.DatabaseLookups import DatabaseLookups


@dataclass
class Billing:
    billing_id: int
    name: str = None
    card_number: str = None
    expiry_date: str = None
    ccv: str = None
    billing_type: str = None
    user_id: int = None

    def create_billing(self, user_id: int) -> 'Billing':
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise errors.InternalError  # change with mysql errors

        # attempt to create billing object
        self.user_id = user_id
        database.insert(self, 'billing', ('billing_id', 'name', 'billing_type'))  # create query

        try:
            billing_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:
            if ie.errno == 1452:  # cannot solve gracefully
                raise ie

            # return billing data, get billing type first
            database.clear()
            database.select(('billing_type_id',), 'billing_type')
            database.where('billing_type_name = %s', 'Out')
            billing_type_id = database.run()

            # get billing data
            database.clear()
            database.select(('billing_id', ), 'billing')
            database.where('card_number = %s', self.card_number)
            database.ampersand('ccv = %s', self.ccv)

            billing_id = database.run()
            self.billing_id = billing_id

            return self

        # set billing_id
        self.billing_id = billing_id

        # clear database tool
        database.clear()

        return self

    def update_billing(self, user_id: int):
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

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Billing):
            remap = {
                "CCname": obj.name,
                "CCNumber": obj.card_number,
                "expirydate": obj.expiry_date,
                "cvv": obj.ccv,
                "billing_type": obj.billing_type
            }
            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        return Billing(billing_id=obj.get('billing_id'), name=obj.get('CCName'), card_number=obj.get('CCNumber'),
                       expiry_date=obj.get('expiryDate'), ccv=obj.get('CVV'), billing_type=obj.get('billingType'))
