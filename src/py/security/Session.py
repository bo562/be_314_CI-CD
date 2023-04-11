"""
py that describes the session object, with supporting functions
"""
from dataclasses import dataclass
from hashlib import sha256
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseStatus import DatabaseStatus
from mysql.connector import errors


@dataclass
class Session:
    session_id: int = None
    access_token: str = None
    expiry_date: str = None
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
        database.clear()
        database.insert(self, 'session', ('session_id',))  # create query

        try:
            self.session_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:
            return None

        return self

    @staticmethod
    def generate_access_token(refresh_token: str):
        to_hash = refresh_token
        hashed = sha256(to_hash.encode('utf-8')).hexdigest()

        return hashed
