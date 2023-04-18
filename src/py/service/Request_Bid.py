"""
py that holds all details regarding Offer
"""
from datetime import datetime
from dataclasses import dataclass

from service.Bid_Status import Bid_Status
from user.Professional import Professional
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseStatus import DatabaseStatus
from util.handling.errors.database.DatabaseConnectionError import DatabaseConnectionError
from util.handling.errors.database.NoDatabaseObjectFound import NoDatabaseObjectFound


@dataclass
class Request_Bid:
    request_bid_id: int = None
    request_id: int = None
    professional_id: int = None
    amount: float = None
    sent_date: datetime = None
    accepted_by_client_date: datetime = None
    professional_cancelled_date: datetime = None
    bid_status_id: int = None

    def create_offer(self):
        pass

    def update_offer(self):
        pass

    @staticmethod
    def get_request_bid(request_bid_id: int) -> 'Request_Bid':
        # create database session
        database = Database.database_handler(DatabaseLookups.User)

        # check if session is connected
        if database.status is not DatabaseStatus.Connected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise DatabaseConnectionError(table='request', query=None, database_object=None)

        # create query for database connection
        database.select(('request_bid_id', 'request_id', 'professional_id', 'amount', 'sent_date', 'bid_status_id',
                         'request_status_id'), 'request')
        database.where('request_bid_id = %s', request_bid_id)

        # try to run query
        result = database.run()

        # if nothing is found return error
        if len(result) == 0:
            query = database.review_query()
            database.clear()
            database.disconnect()
            raise NoDatabaseObjectFound(table='request_bid', query=query, database_object=None)

        # parse into request object
        request_bid = Request_Bid(request_bid_id=result[0][0], request_id=result[0][1], professional_id=result[0][2],
                                  amount=result[0][3], sent_date=result[0][4], bid_status_id=result[0][5])

        return request_bid

    @staticmethod
    def get_by_request_id(request_id: int) -> ['Request_Bid']:
        database = Database.database_handler(DatabaseLookups.User)

        # check if session is connected
        if database.status is not DatabaseStatus.Connected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise DatabaseConnectionError(table='request', query=None, database_object=None)

        # create query for database connection
        database.select(('request_bid_id', 'request_id', 'professional_id', 'amount', 'sent_date', 'bid_status_id'),
                        'request_bid')
        database.where('request_id = %s', request_id)

        # run database
        results = database.run()

        # if no objects found
        if len(results) == 0:
            return None

        # iterate through results and create request bids
        request_bids = []
        for result in results:
            request_bids.append(Request_Bid(request_bid_id=result[0], request_id=result[1], professional_id=result[2],
                                            amount=result[3], sent_date=result[4], bid_status_id=result[5]))

        return request_bids

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Request_Bid):
            remap = {
                "applicationID": obj.request_bid_id,
                "requestID": obj.request_id,
                "offerDate": obj.sent_date,
                "userID": Professional.get_by_professional_id(obj.professional_id).user_id,
                "cost": obj.amount
            }

            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        # convert user_id for professional to professional_id
        print(obj.get('professionalID'))
        professional_id = Professional.get_professional(obj.get('professionalID')).professional_id

        # get bid status id
        if obj.get('applicationStatus') is not None:
            bid_status_id = Bid_Status.get_by_status_name(obj.get('applicationStatus')).bid_status_id

        else:
            bid_status_id = None

        # create object
        return Request_Bid(request_id=obj.get('requestID'), sent_date=obj.get('requestDate'),
                           professional_id=professional_id, amount=obj.get('cost'), bid_status_id=bid_status_id)
