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
        database.insert(self, 'billing', ('billing_id', 'billing_type'))  # create query

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

            self.billing_id = database.run()

            return self

        # set billing_id
        self.billing_id = billing_id

        # clear database tool
        database.clear()

        return self

    def update_billing(self, user_id: int):
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
        database.update(self, 'billing', ('billing_id', 'billing_type'))
        database.where('user_id = %s', self.user_id)

        try:  # attempt to return
            self.billing_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:
            raise ie

        # clear database tool
        database.clear()

        return self

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Billing):
            remap = {
                "CCname": obj.name,
                "CCNumber": obj.card_number,
                "expiryDate": obj.expiry_date,
                "CCV": obj.ccv,
                "billingType": obj.billing_type
            }
            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        return Billing(billing_id=obj.get('billing_id'), name=obj.get('CCName'), card_number=obj.get('CCNumber'),
                       expiry_date=obj.get('expiryDate'), ccv=obj.get('CCV'), billing_type=obj.get('billingType'))
