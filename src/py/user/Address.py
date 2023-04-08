"""
class for address data structure
"""
from dataclasses import dataclass
from util.database import Database as db, DatabaseLookups as dl


@dataclass
class Address:
    address_id: int
    street_number: str = None
    street_name: str = None
    suburb: str = None
    postcode: str = None

    def create_address(self, user_id: int):
        try:
            database = db.Database.database_handler(dl.DatabaseLookups.user.value)  # create database to connect to
            database.database_connect()  # connect to database
            query = "SELECT user_id FROM project.user WHERE user_id=%d"
            query_data = user_id
            validation_check = database.database_query(query, query_data)
            if not isinstance(validation_check, int) or validation_check < 0:
                return "invalid id"
        except Exception as e:
            print("Database Connection Error")
        query = ("INSERT INTO project.address "
                 "(user_id, street_number, street_name, suburb, postcode) "
                 "VALUES (%d, %s, %s, %s, %s)")
        query_data = (user_id, self.street_number, self.street_name, self.suburb, self.postcode)
        database.database_query(query, query_data)
        query = "SELECT address_id FROM project.address WHERE user_id=%d"
        query_data = user_id
        temp_address_id = database.database_query(query, query_data)
        if temp_address_id is None:
            return "address creation failed"
        self.address_id = temp_address_id
        database.database_disconnect()

    def update_address(self, user_id: int):
        try:
            database = db.Database.database_handler(dl.DatabaseLookups.user.value)  # create database to connect to
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
        return Address(address_id=-1, street_number=obj.get('streetNumber'),
                       street_name=obj.get('streetName'), suburb=obj.get('suburb'), postcode=obj.get('postcode'))
