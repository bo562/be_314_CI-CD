"""
py that describes the session object, with supporting functions
"""
from dataclasses import dataclass
from hashlib import sha256
from datetime import datetime
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseStatus import DatabaseStatus
from mysql.connector import errors


@dataclass
class Session:
    session_id: int = None
    access_token: str = None
    expiry_date: datetime = None
    authorisation_id: int = None

    def create_session(self, authorisation_id: int):
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise errors.InternalError  # change with mysql errors

        # if user_id null set user_id
        if self.authorisation_id is None:
            self.authorisation_id = authorisation_id

        # attempt to create authorisation object
        database.insert(self, 'session', ('session_id',))  # create query

        try:
            self.session_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:
            return None

        return self

    # method that returns whether or not a access_token is valid
    @staticmethod
    def validate_session(access_token: str) -> bool:
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)

        # check if database connected
        if database.status == DatabaseStatus.Disconnected:
            database.connect()

        # check whether the session is invalidated
        database.select(('session_id',), 'session')
        database.where('access_token = %s', access_token)
        database.where('expiry_date > %s', datetime.now())

        # try running the query
        try:
            results = database.run()

        except Exception as e:
            raise e

        # check if session_id is returned based on expiry date
        if results[0][0] is None:
            return True

        else:
            return False



    @staticmethod
    def generate_access_token(refresh_token: str):
        to_hash = refresh_token
        hashed = sha256(to_hash.encode('utf-8')).hexdigest()

        return hashed
