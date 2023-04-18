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
from util.handling.errors.database.NoDatabaseObjectFound import NoDatabaseObjectFound


@dataclass
class Request:
    request_id: int = None
    request_date: datetime = None
    start_date: datetime = None
    completion_date: datetime = None
    instruction: str = None
    postcode: int = None
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

        return Request.get_request(self.request_id)

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

    @staticmethod
    def get_request(request_id: int) -> 'Request':
        # create database session
        database = Database.database_handler(DatabaseLookups.User)

        # check if session is connected
        if database.status is not DatabaseStatus.Connected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise DatabaseConnectionError(table='request', query=None, database_object=None)

        # create query for database connection
        database.select(('request_id', 'request_date', 'instruction', 'postcode', 'client_id', 'professional_id', 'service_id',
                         'request_status_id'), 'request')
        database.where('request_id = %s', request_id)

        # try to run query
        result = database.run()

        # if nothing is found return error
        if len(result) == 0:
            query = database.review_query()
            database.clear()
            database.disconnect()
            raise NoDatabaseObjectFound(table='request', query=query, database_object=None)

        # parse into request object
        request = Request(request_id=result[0][0], request_date=result[0][1], instruction=result[0][2],
                          postcode=result[0][3], client_id=result[0][4], professional_id=result[0][5],
                          service_id=result[0][6], request_status_id=result[0][7])

        # get request_bids
        request.request_bids = Request_Bid.get_by_request_id(request.request_id)

        # clean up instance
        database.clear()
        database.disconnect()

        return request

    # returns an array
    @staticmethod
    def get_client_requests(client_id: int):
        # create database session
        database = Database.database_handler(DatabaseLookups.User)

        # check if session is connected
        if database.status is not DatabaseStatus.Connected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise DatabaseConnectionError(table='request', query=None, database_object=None)

        # create query for database connection
        database.select(('request_id',), 'request')
        database.where('client_id = %s', client_id)

        # try to run query
        results = database.run()

        # if nothing is found return error
        if len(results) == 0:
            query = database.review_query()
            database.clear()
            database.disconnect()
            raise NoDatabaseObjectFound(table='request', query=query, database_object=None)

        # parse into request object
        requests = []
        for result in results:
            requests.append(Request.get_request(result[0]))

        return requests

    @staticmethod
    def get_client_requests(professional_id: int):
        # create database session
        database = Database.database_handler(DatabaseLookups.User)

        # check if session is connected
        if database.status is not DatabaseStatus.Connected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise DatabaseConnectionError(table='request', query=None, database_object=None)

        # create query for database connection
        database.select(('request_id',), 'request')
        database.where('professional_id = %s', professional_id)

        # try to run query
        results = database.run()

        # if nothing is found return error
        if len(results) == 0:
            return None

        # parse into request object
        requests = []
        for result in results:
            requests.append(Request.get_request(result[0]))

        return requests

    @staticmethod
    def get_by_postcode(postcode: int) -> ['Request']:
        # create database session
        database = Database.database_handler(DatabaseLookups.User)

        # check if session is connected
        if database.status is not DatabaseStatus.Connected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise DatabaseConnectionError(table='request', query=None, database_object=None)

        # create query for database connection
        database.select(('request_id',), 'request')
        database.where('postcode = %s', postcode)

        # try to run query
        results = database.run()

        # if nothing is found return error
        if len(results) == 0:
            return None

        # parse into request object
        requests = []
        for result in results:
            requests.append(Request.get_request(result[0]))

        return requests

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Request):
            if obj.professional_id is not None:
                professional_id = Professional.get_by_professional_id(obj.professional_id).user_id
            else:
                professional_id = None

            # revert ids into names for api results
            service_name = Service.get_by_service_id(obj.service_id).service_name
            status_name = Request_Status.get_request_status_by_id(obj.request_status_id).status_name
            client_id = Client.get_by_client_id(obj.client_id).client_id

            remap = {
                "requestID": obj.request_id,
                "requestDate": obj.request_date,
                "serviceType": service_name,
                "requestStatus": status_name,
                "jobDescription": obj.instruction,
                "postcode": obj.postcode,
                "clientID": client_id,
                "professionalID": professional_id,
                "applications": obj.request_bids if obj.request_bids is not None else None
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
                       service_id=service_id, client_id=client_id, postcode=obj.get('postcode'),
                       professional_id=professional_id, request_status_id=request_status_id,
                       request_bids=obj.get('applications'))
