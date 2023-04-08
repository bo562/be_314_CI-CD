"""
class for address data structure
"""
from dataclasses import dataclass
from util.database.DatabaseLookups import DatabaseLookups
from util.database.Database import Database
from util.database.DatabaseStatus import DatabaseStatus
from mysql.connector import errors


@dataclass
class Address:
    address_id: int
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
        except errors.IntegrityError as ie:  # in case that user already exists
            if ie.errno == 1452:  # cannot solve gracefully
                raise ie

            # constructing query to return already created user
            database.clear()
            database.select(('address_id', ), 'address')
            database.where('user_id = %s', self.user_id)
            address_id = database.run()[0][0]

        self.address_id = address_id

        # clear database tool
        database.clear()

        return self

    def update_address(self, user_id: int):
        try:
            database = Database.database_handler(DatabaseLookups.user.value)  # create database to connect to
            database.database_connect()  # connect to database
            query = "SELECT user_id FROM project.user WHERE user_id=%d"
            query_data = user_id
            validation_check = database.database_query(query, query_data)
            if not isinstance(validation_check, int) or validation_check < 0:
                return "invalid id"
        except Exception as e:
            print("Database Connection Error")
        query = ("UPDATE project.address "
                 "SET street_number = %s, street_name = %s, suburb = %s, postcode = %s "
                 "WHERE user_id = %d")
        query_data = ( self.street_number, self.street_name, self.suburb, self.postcode, user_id)
        database.database_query(query, query_data)
        query = "SELECT address_id FROM project.address WHERE user_id=%d"
        query_data = user_id
        temp_address_id = database.database_query(query, query_data)
        if temp_address_id is None:
            return "address update failed"
        self.address_id = temp_address_id
        database.database_disconnect()

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Address):
            remap = {
                "streetname": obj.street_name,
                "streetnumber": obj.street_number,
                "suburb": obj.suburb,
                "postcode": obj.postcode
            }

            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        return Address(address_id=obj.get('address_id'), street_number=obj.get('streetNumber'),
                       street_name=obj.get('streetName'), suburb=obj.get('suburb'), postcode=obj.get('postcode'))
