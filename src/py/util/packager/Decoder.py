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


class Decoder:
    __object: str
    __class_type: type

    def __init__(self, obj, class_type: type):
        # pass variables to parent class
        self.__object = obj
        self.__class_type = class_type

    def deserialize(self):
        return json.loads(self.__object, object_hook=Decoder.default)

    # based on object type call correct FromAPI method
    @staticmethod
    def default(obj: object):
        if 'address' not in obj.keys():
            print(obj)
            return Address.FromAPI(obj)
        elif 'userID' in obj.keys():
            print(obj)
            return User.FromAPI(obj)
        else:
            print(obj)
            return obj
