"""
py that utlises orjson to package DTO classes for return to Front-End and deserialse JSONs from FRONT end
for manipulation in database
"""

import orjson
import json
from user.User import User
from user.Address import Address
from user.Billing import Billing
from user.Client import Client
from user.Professional import Professional
from user.Subscription import Subscription


class Encoder:
    __object: object

    def __init__(self, obj: object):
        self.__object = obj

    def serialize(self) -> bytes:
        return orjson.dumps(self.__object,
                            option=orjson.OPT_PASSTHROUGH_DATACLASS,
                            default=Encoder.default)

    # based on object type call correct ToAPI method
    @staticmethod
    def default(obj: object):
        if isinstance(obj, User):
            return User.ToAPI(obj)

        elif isinstance(obj, Address):
            return Address.ToAPI(obj)

        elif isinstance(obj, Billing):
            return Billing.ToAPI(obj)

        elif isinstance(obj, Client):
            return Client.ToAPI(obj)

        elif isinstance(obj, Professional):
            return Professional.ToAPI(obj)

        raise TypeError
