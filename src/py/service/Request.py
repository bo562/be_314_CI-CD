"""
py that handles data for requests type
"""
from datetime import datetime
from dataclasses import dataclass
from service.Service import Service
from util.database.DatabaseLookups import DatabaseLookups
from util.database.Database import Database
from util.database.DatabaseStatus import DatabaseStatus
from mysql.connector import errors

from util.handling.errors.database.DatabaseObjectAlreadyExists import DatabaseObjectAlreadyExists


@dataclass()
class Request:
    request_id: int
    request_date: datetime = None
    start_date: datetime = None
    completion_date: datetime = None
    instruction: str = None
    client_id: int = None
    professional_id: int = None
    service_id: int = None
    request_status_id: int = None
    status_name: str = None

    def create_request(self):
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise errors.InternalError  # change with mysql errors
            # attempt to create address row
        database.select(('request_status_id',), 'request_status')
        database.where('status_name = %s', self.status_name)
        self.request_status_id = database.run()[0][0]
        database.clear()

        # attempt to create address row
        database.insert(self, 'request', ('request_id', 'professional_id', 'completion_date', 'request_status_id', 'status_name',))

        try:
            address_id = database.run()
            database.commit()
        except errors.IntegrityError as ie:  # in case that user already exists
            # revert changes and remove lock
            database.rollback()

            # clear tool
            query = database.review_query()
            database.clear()

            if ie.errno == 1452:  # cannot solve gracefully
                raise DatabaseObjectAlreadyExists(status_code=400, table='request', query=query, database_object=self,
                                                  message=ie.msg)



        self.address_id = address_id

        # clear database tool
        database.clear()

        return self

    def update_request(self):
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise errors.InternalError  # change with mysql errors
        if self.status_name is not None:
            try:
                database.select(('request_status_id',), 'request_status')
                database.where('status_name = %s', self.status_name)
                self.request_status_id = database.run()[0][0]
                database.clear()
            except errors.IntegrityError as ie:  # in case that user already exists
                if ie.errno == 1452:  # cannot solve gracefully
                    raise ie
        # create query
        database.clear()
        database.update(self, 'request', ('request_id', 'status_name'))
        database.where('request_id = %s', self.request_id)

        try:  # attempt to return
            database.run()
            database.commit()

        except errors.IntegrityError as ie:
            raise ie

        # clear database tool
        database.clear()

        return self

    def get_request(self):
        pass


    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Request):
            remap = {
                "requestID": obj.request_id,
                "requestDate": obj.request_date,
                "serviceType": Service.get_by_service_id(obj.service_id).service_name
            }

    @staticmethod
    def FromAPI(obj):
        # get client_id from passed user_id