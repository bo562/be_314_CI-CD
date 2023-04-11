"""
py that describes authorisation object with supporting functions

Error handling will need to be fleshed out
"""
import datetime
from dataclasses import dataclass

from mysql.connector import Error

from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseStatus import DatabaseStatus
from mysql.connector import errors
from user import User
from hashlib import sha256


@dataclass
class Authorisation:
    authorisation_id: int = None
    refresh_token: str = None
    number_of_uses: int = 0
    invalidated: str = 'N'
    user_id: int = None

    @staticmethod
    def generate_refresh_token(user_id: int):
        to_hash = str(user_id) + datetime.datetime.now().strftime("%d/%m/%YT%H:%M:%S")
        hashed = sha256(to_hash.encode('utf-8')).hexdigest()

        return hashed

    # general functions
    def create_authorisation(self, user_id: int):
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise errors.InternalError  # change with mysql errors

        # if user_id null set user_id
        if self.user_id is None:
            self.user_id = user_id

        # attempt to create authorisation object
        database.clear()
        database.insert(self, 'authorisation', ('authorisation_id',))  # create query

        try:
            self.authorisation_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:
            return None

        return self

    def update_authorisation(self):
        pass

    def update_field(self, attribute: str, value):
        pass

    # specialised functions
    def invalidate(self):
        pass

    @staticmethod
    def get_authorisation(user_id: int):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # check if current authorisation exists
        database.clear()
        database.select(('authorisation_id', 'refresh_token', 'number_of_uses', 'invalidated', 'user_id'),
                        'authorisation')
        database.where('user_id = %s', user_id)
        database.ampersand('invalidated = %s', 'N')

        # try to get authorisation
        authorisation = None
        try:
            results = database.run()

        except Exception as e:
            raise e

        if len(results) > 0:
            authorisation = Authorisation(authorisation_id=results[0][0], refresh_token=results[0][1],
                                          number_of_uses=results[0][1], invalidated=results[0][2],
                                          user_id=results[0][1])

        return authorisation

    @staticmethod
    def validate_credentials(email_address, password) -> int:
        # create connection to database
        database = Database.database_handler(DatabaseLookups.User)

        # using underlying query handler to save time with creating user object instead
        # if email and password match return user_id
        database.clear()
        database.select(('user_id',), 'user')
        database.where('email_address = %s', email_address)
        database.ampersand('password = %s', password)
        result = database.run()

        # if result is empty then there is no match
        if len(result) == 0:
            return None

        else:
            return int(result[0][0])
