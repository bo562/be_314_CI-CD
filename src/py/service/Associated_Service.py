"""
py that describes the DTO that holds data for the associated_service table in the database
"""
from dataclasses import dataclass
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseStatus import DatabaseStatus
from mysql.connector import errors

@dataclass
class Associated_Service:
    provided_service_id: int = None
    service_id: int = None
    professional_id: int = None

    def create_associated_service(self, professional_id: int):
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise errors.InternalError  # change with mysql errors

        # if user_id null set user_id
        if self.professional_id is None:
            self.professional_id = professional_id

        # attempt to create address row
        database.clear()
        database.insert(self, 'associated_service', ('provided_service_id',))

        try:
            self.provided_service_id = database.run()
            database.commit()
        except errors.IntegrityError as ie:  # in case that user already exists
            if ie.errno == 1452:  # cannot solve gracefully
                raise ie

            # constructing query to return already created user
            database.clear()
            database.select(('provided_service_id', ), 'associated_service')
            database.where('professional_id = %s', self.user_id)
            self.provided_service_id = database.run()[0][0]

        # clear database tool
        database.clear()

        return self
