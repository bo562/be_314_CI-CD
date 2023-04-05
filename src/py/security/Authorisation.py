"""
py that describes authorisation object with supporting functions

Error handling will need to be fleshed out
"""
import datetime
from dataclasses import dataclass

from mysql.connector import Error

from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
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
    def create_authorisation(self, email_address, password):
        # connect to database
        try:
            database = Database.database_handler(DatabaseLookups.User.value)
            database.database_connect()
        except Exception as e:  # simple error handling
            raise e

        # find user_id from username and password
        query = "SELECT user_id FROM Project.user WHERE email_address = %s AND password = %s"
        try:
            results = database.database_query(query, (email_address, password))
        except Error as err:  # simple error handling
            raise err

        self.user_id = results[0][0]
        print(self.user_id)

        # create refresh token
        self.refresh_token = Authorisation.generate_refresh_token(self.user_id)

        # create query, params will be values of authorisation class
        query = "INSERT INTO authorisation (refresh_token, number_of_uses, invalidated, user_id)" \
                "VALUES(%s, %s, %s, %s)"

        # try to insert into database
        try:
            results = database.database_query(query, (self.refresh_token, self.numberof_uses,
                                                      self.invalidated, self.user_id))
        except Error as err:  # simple error handling
            raise err

    def update_authorisation(self):
        pass

    def update_field(self, attribute: str, value):
        pass

    # specialised functions
    def invalidate(self):
        pass
