"""
py that describes authorisation object with supporting functions

Error handling will need to be fleshed out
"""
import datetime
from dataclasses import dataclass

from mysql.connector import Error

from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseAction import DatabaseAction
from user import User
from hashlib import sha256


@dataclass
class Authorisation:
    authorisation_id: int = None
    refresh_token: str = None
    numberof_uses: int = 0
    invalidated: str = 'N'
    user_id: int = None

    @staticmethod
    def generate_refresh_token(user_id: int):
        to_hash = str(user_id) + datetime.datetime.now().strftime("%d/%m/%YT%H:%M:%S")
        hashed = sha256(to_hash.encode('utf-8')).hexdigest()

        return hashed

    # general functions
    def create_authorisation(self):
        pass

    def update_authorisation(self):
        pass

    def update_field(self, attribute: str, value):
        pass

    # specialised functions
    def invalidate(self):
        pass

    @staticmethod
    def validate_credentials(email_address, password) -> int:
        # create connection to database
        database = Database.database_handler(DatabaseLookups.User)

        # using underlying query handler to save time with creating user object instead
        # if email and password match return user_id
        database.clear()
        database.select(('user_id',), 'user')
        database.where('email_address = %s', email_address)
        result = database.run()

        # if result is empty then there is no match
        if len(result) == 0:
            return int(result)

        else:
            return None
