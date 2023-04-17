"""
py that describes the DTO for request_status in the database
"""
from dataclasses import dataclass
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseStatus import DatabaseStatus
from util.handling.errors.database.DatabaseError import DatabaseError
from util.handling.errors.database.NoDatabaseObjectFound import NoDatabaseObjectFound


@dataclass
class Request_Status:
    request_status_id: int = None
    status_name: str = None

    @staticmethod
    def get_request_status_by_id(request_status_id: int):
        # create database session
        database = Database.database_handler(DatabaseLookups.User)

        # check if connected to database
        if database.status is not DatabaseStatus.Connected:
            database.connect()

        # create query to retrieve request_status
        database.select(('request_status_id', 'status_name'), 'request_status')
        database.where('request_status_id = %s', request_status_id)

        # run database query and catch errors
        try:
            result = database.run()
            database.commit()

        except Exception as e:
            # clean up and record errors after database failure
            query = database.review_query()
            database.clear()
            database.disconnect()

            raise DatabaseError(status_code='500', table='request_status', query=query, database_object=None,
                                message='Could not retrieve request_status {}'.format(request_status_id))

        # check if request_status exists and raise error if it does not
        if len(result) == 0:
            query = database.review_query()
            database.clear()
            database.disconnect()
            raise NoDatabaseObjectFound(status_code='500', table='request_status', query=query, database_object=None,
                                        message='request_status {} does not exist'.format(request_status_id))

        return Request_Status(request_status_id=result[0][0], status_name=result[0][1])

    @staticmethod
    def get_request_status_by_name(status_name: str):
        # create database session
        database = Database.database_handler(DatabaseLookups.User)

        # check if connected to database
        if database.status is not DatabaseStatus.Connected:
            database.connect()

        # create query to retrieve request_status
        database.select(('request_status_id', 'status_name'), 'request_status')
        database.where('status_name = %s', status_name)

        # run database query and catch errors
        try:
            result = database.run()
            database.commit()

        except Exception as e:
            # clean up and record errors after database failure
            query = database.review_query()
            database.clear()
            database.disconnect()

            raise DatabaseError(status_code='500', table='request_status', query=query, database_object=None,
                                message='Could not retrieve request_status {}'.format(status_name))

        # check if request_status exists and raise error if it does not
        if len(result) == 0:
            query = database.review_query()
            database.clear()
            database.disconnect()
            raise NoDatabaseObjectFound(status_code='500', table='request_status', query=query, database_object=None,
                                        message='request_status {} does not exist'.format(status_name))

        return Request_Status(request_status_id=result[0][0], status_name=result[0][1])
