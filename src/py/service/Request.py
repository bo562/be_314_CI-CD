"""
py that handles data for requests type
"""
from datetime import datetime
from dataclasses import dataclass
from service.Service import Service
from user.Client import Client
from user.Professional import Professional
from util.database.DatabaseLookups import DatabaseLookups
from util.database.Database import Database
from util.database.DatabaseStatus import DatabaseStatus
from service.Request_Status import Request_Status
from service.Request_Bid import Request_Bid
from user.User import User
from mysql.connector import errors

from util.handling.errors.database.DatabaseConnectionError import DatabaseConnectionError
from util.handling.errors.database.DatabaseObjectAlreadyExists import DatabaseObjectAlreadyExists
from util.handling.errors.database.FailedToCreateDatabaseObject import FailedToCreateDatabaseObject
from util.handling.errors.database.FailedToUpdateDatabaseObject import FailedToUpdateDatabaseObject


@dataclass
class Request:
    request_id: int = None
    request_date: datetime = None
    start_date: datetime = None
    completion_date: datetime = None
    instruction: str = None
    client_id: int = None
    professional_id: int = None
    service_id: int = None
    request_status_id: int = None
    request_bids: ['Request_Bid'] = None

    def create_request(self):
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise DatabaseConnectionError(table='request', query=None, database_object=None)

        # construct query for creation
        database.insert(self, 'request', ('request_id', 'start_date', 'completion_date', 'request_bids'))

        # try to run query
        try:
            self.request_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:  # in case that change violates consistency constraints
            # clean up instance and rollback to remove lock
            database.rollback()
            query = database.review_query()
            database.clear()
            database.disconnect()

            # if there is an integrity error
            if ie.errno == 1452:  # cannot solve gracefully
                # raise error
                raise DatabaseObjectAlreadyExists(table='user', query=query, database_object=self)

            # some other consistency constraint check
            raise FailedToCreateDatabaseObject(table='user', query=query, database_object=self)

        # clear database tool
        database.clear()
        database.disconnect()

        return self

    def update_request(self):
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise DatabaseConnectionError(table='request', query=None, database_object=None)

        # construct query for creation
        database.insert(self, 'request', ('request_id', 'start_date', 'completion_date', 'request_bids'))

        # try to run query
        try:
            self.request_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:  # in case that change violates consistency constraints
            # clean up instance and rollback to remove lock
            database.rollback()
            query = database.review_query()
            database.clear()
            database.disconnect()

            # if there is an integrity error
            if ie.errno == 1452:  # cannot solve gracefully
                # raise error
                raise DatabaseObjectAlreadyExists(table='user', query=query, database_object=self)

            # some other consistency constraint check
            raise FailedToUpdateDatabaseObject(table='user', query=query, database_object=self)

        # clear database tool
        database.clear()
        database.disconnect()

        return self

    def get_request(self):
        pass

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Request):
            remap = {
                "requestID": obj.request_id,
                "requestDate": obj.request_date,
                "serviceType": Service.get_by_service_id(obj.service_id).service_name,
                "requestStatus": Request_Status.get_request_status_by_id(obj.request_status_id).status_name,
                "jobDescription": obj.instruction,
                "clientID": Client.get_by_client_id(obj.client_id).user_id,
                "professionalID": Professional.get_by_professional_id(obj.professional_id).user_id,
                "applications": obj.request_bids
            }

            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        # get required ids
        client_id = User.get_user(obj.get('clientID')).client.client_id
        request_status_id = Request_Status.get_request_status_by_name(obj.get('requestStatus')).request_status_id
        service_id = Service.get_by_service_name(obj.get('serviceType')).service_id

        # check if professional_id exists and retrieve
        if obj.get('professionalID') is not None:
            professional_id = Professional.get_professional(obj.get('professionalID')).professional_id
        else:
            professional_id = None

        # return request object
        return Request(request_id=None, request_date=obj.get('requestDate'), instruction=obj.get('jobDescription'),
                       service_id=service_id, client_id=client_id, professional_id=professional_id,
                       request_status_id=request_status_id, request_bids=obj.get('applications'))
