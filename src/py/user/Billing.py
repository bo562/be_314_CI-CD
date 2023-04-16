"""
py class for credit card data structure
"""
from dataclasses import dataclass
from mysql.connector import errors
from util.database.Database import Database
from util.database.DatabaseStatus import DatabaseStatus
from util.database.DatabaseLookups import DatabaseLookups
from util.handling.errors.database.DatabaseObjectAlreadyExists import DatabaseObjectAlreadyExists
from util.handling.errors.database.FailedToCreateDatabaseObject import FailedToCreateDatabaseObject
from util.handling.errors.database.FailedToUpdateDatabaseObject import FailedToUpdateDatabaseObject


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

        # set billing_id
        self.billing_id = billing_id

        # clear database tool and disconnect
        database.clear()
        database.disconnect()

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

        # clear database tool and disconnect
        database.clear()
        database.disconnect()

        return self

    def delete_billing(self) -> bool:
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()

        database.delete('billing')
        database.where('billing_id = %s', self.billing_id)

        try:
            database.run()
            database.commit()
        except Exception as e:
            database.rollback()
            return False

        return True

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
