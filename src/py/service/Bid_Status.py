"""
py that describes bid_status DTO from database
"""
from dataclasses import dataclass

from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseStatus import DatabaseStatus
from util.handling.errors.database.DatabaseError import DatabaseError
from util.handling.errors.database.NoDatabaseObjectFound import NoDatabaseObjectFound


@dataclass
class Bid_Status:
    bid_status_id: int = None
    status_name: str = None

    @staticmethod
    def get_by_status_id(bid_status_id: int):
        # create database session
        database = Database.database_handler(DatabaseLookups.User)

        # check database connection
        if database.status is not DatabaseStatus.Connected:
            database.connect()

        else:
            raise DatabaseError(status_code='500', table=None, query=None, database_object=None,
                                message='Could not connect to Database')

        # construct query to retrive bid status from provided id
        database.select(('bid_status_id', 'status_name'), 'bid_status')
        database.where('bid_status_id = %s', bid_status_id)

        # attempt to run query
        try:
            result = database.run()

        except Exception as e:
            # clean up session
            query = database.review_query()
            database.clear()
            database.disconnect()
            raise DatabaseError(status_code='500', table='bid_status', query=query, database_object=None,
                                message='Could not connect to Database')

        # parse result and return
        if len(result) == 0:
            query = database.review_query()
            database.clear()
            database.disconnect()
            raise NoDatabaseObjectFound(status_code='500', table='bid_status', query=query, database_object=None)

        return Bid_Status(bid_status_id=result[0][0], status_name=result[0][1])

    @staticmethod
    def get_by_status_name(status_name: str):
        # create database session
        database = Database.database_handler(DatabaseLookups.User)

        # check database connection
        if database.status is not DatabaseStatus.Connected:
            database.connect()

        else:
            raise DatabaseError(status_code='500', table=None, query=None, database_object=None,
                                message='Could not connect to Database')

        # construct query to retrive bid status from provided id
        database.select(('bid_status_id', 'status_name'), 'bid_status')
        database.where('status_name = %s', status_name)

        # attempt to run query
        try:
            result = database.run()

        except Exception as e:
            # clean up session
            query = database.review_query()
            database.clear()
            database.disconnect()
            raise DatabaseError(status_code='500', table='bid_status', query=query, database_object=None,
                                message='Could not connect to Database')

        # parse result and return
        if len(result) == 0:
            query = database.review_query()
            database.clear()
            database.disconnect()
            raise NoDatabaseObjectFound(status_code='500', table='bid_status', query=query, database_object=None)

        return Bid_Status(bid_status_id=result[0][0], status_name=result[0][1])
