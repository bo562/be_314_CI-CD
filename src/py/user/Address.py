"""
class for address data structure
"""
from dataclasses import dataclass
from util.database.DatabaseLookups import DatabaseLookups
from util.database.Database import Database
from util.database.DatabaseStatus import DatabaseStatus
from mysql.connector import errors

from util.handling.errors.database.DatabaseObjectAlreadyExists import DatabaseObjectAlreadyExists
from util.handling.errors.database.FailedToCreateDatabaseObject import FailedToCreateDatabaseObject
from util.handling.errors.database.FailedToUpdateDatabaseObject import FailedToUpdateDatabaseObject


@dataclass
class Address:
    address_id: int = None
    street_number: str = None
    street_name: str = None
    suburb: str = None
    postcode: str = None
    user_id: int = None

    def create_address(self, user_id: int):
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise errors.InternalError  # change with mysql errors

        # if user_id null set user_id
        if self.user_id is None:
            self.user_id = user_id

        # attempt to create address row
        database.insert(self, 'address', ('address_id',))

        try:
            address_id = database.run()
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

    def update_address(self, user_id: int):
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
        database.update(self, 'address', ('address_id',))
        database.where('user_id = %s', self.user_id)

        try:  # attempt to return
            self.address_id = database.run()
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

    def delete_address(self):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()

        database.delete('address')
        database.where('address_id = %s', self.address_id)

        try:
            database.run()
            database.commit()
        except Exception as e:
            return False

        return True

    @staticmethod
    def get_address(user_id: int):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # get user object
        database.clear()
        database.select(('address_id', 'street_number', 'street_name', 'suburb', 'postcode'),
                        'address')
        database.where('user_id = %s', user_id)

        # try to get authorisation
        address = None
        try:
            results = database.run()

        except Exception as e:
            raise e

        if len(results) > 0:
            address = Address(address_id=results[0][0], street_number=results[0][1], street_name=results[0][2],
                        suburb=results[0][3], postcode=results[0][4])

        return address

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Address):
            remap = {
                "streetName": obj.street_name,
                "streetNumber": obj.street_number,
                "suburb": obj.suburb,
                "postcode": obj.postcode
            }

            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        return Address(address_id=obj.get('address_id'), street_number=obj.get('streetNumber'),
                       street_name=obj.get('streetName'), suburb=obj.get('suburb'), postcode=obj.get('postcode'))
