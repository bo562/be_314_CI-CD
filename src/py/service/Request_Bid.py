"""
py that holds all details regarding Offer
"""
from datetime import datetime
from dataclasses import dataclass

from service.Bid_Status import Bid_Status
from user.Professional import Professional


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
