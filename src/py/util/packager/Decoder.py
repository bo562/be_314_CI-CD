"""
py that enables smarter decoding of json objects into specified classes
"""

import orjson
import json

from service.Request import Request
from service.Request_Bid import Request_Bid
from user.User import User
from user.Address import Address
from user.Billing import Billing
from user.Client import Client
from user.Professional import Professional
from user.Subscription import Subscription
from user.User_Question import User_Question


class Decoder:
    __object: str
    __class_type: type

    def __init__(self, obj):
        # pass variables to parent class
        self.__object = obj

    def deserialize(self):
        decoded = json.loads(self.__object, object_hook=Decoder.default)
        return decoded

    # based on object type call correct FromAPI method
    @staticmethod
    def default(obj: dict):
        if 'user_id' in obj.keys():  # checking for main user object
            return User.FromAPI(obj)

        elif 'CCName' in obj.keys() or \
                'CCNumber' in obj.keys() or \
                'expiryDate' in obj.keys() or \
                'CCV' in obj.keys() or \
                'billingType' in obj.keys():  # checking for CCOut field
            return Billing.FromAPI(obj)

        # checking for address field
        elif 'streetName' in obj.keys() or \
                'streetNumber' in obj.keys() or \
                'suburb' in obj.keys() or \
                'postcode' in obj.keys() and 'requestID' not in obj.keys():
            return Address.FromAPI(obj)

        elif 'membershipType' in obj.keys():  # checking for client field
            return Client.FromAPI(obj)

        elif 'CCIn' in obj.keys() or \
                'services' in obj.keys():  # checking for professional field
            return Professional.FromAPI(obj)

        elif 'securityQuestion' in obj.keys():
            return User_Question.FromAPI(obj)

        elif 'requestID' in obj.keys() and 'applicationID' not in obj.keys():
            return Request.FromAPI(obj)

        elif 'applicationID' in obj.keys():
            return Request_Bid.FromAPI(obj)

        else:
            return None
