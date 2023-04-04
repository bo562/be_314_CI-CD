"""
py that describes authorisation object with supporting functions
"""
from dataclasses import dataclass
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from user import User
from hashlib import sha256


@dataclass
class Authorisation:
    authorisation_id: int
    refresh_token: str = None
    numberof_uses: int = None
    invalidated: str = None
    user_id: int = None

    # static functions
    @staticmethod
    def generate_token(user: User):
        # create database connection for queries
        database = Database.database_handler(DatabaseLookups.User.value)
        database.database_connect()

        # create and run query
        query = "SELECT user_id, first_name, last_name FROM Project.User"
        results = database.database_query(query)

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



