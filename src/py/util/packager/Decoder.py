"""
py that enables smarter decoding of json objects into specified classes
"""

import orjson
import json
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

    def __init__(self, obj, class_type: type):
        # pass variables to parent class
        self.__object = obj
        self.__class_type = class_type

    def deserialize(self):
        decoded = json.loads(self.__object, object_hook=Decoder.default)
        return decoded

    # based on object type call correct FromAPI method
    @staticmethod
    def default(obj: object):
        if 'user_id' in obj.keys():  # checking for main user object
            return User.FromAPI(obj)

        elif 'CCName' in obj.keys():  # checking for CCOut field
            return Billing.FromAPI(obj)

        elif 'streetName' in obj.keys():  # checking for address field
            return Address.FromAPI(obj)

        elif 'membershipType' in obj.keys():  # checking for client field
            return Client.FromAPI(obj)

        elif 'CCin' in obj.keys():  # checking for professional field
            return Professional.FromAPI(obj)

        elif 'securityQuestion1' in obj.keys():  # checking for security question field
            return User_Question.FromAPI(obj)

        else:
            return obj
