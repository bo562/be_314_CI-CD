"""
py that utlises orjson to package DTO classes for return to Front-End and deserialse JSONs from FRONT end
for manipulation in database
"""

import orjson
import user
from service.Request import Request
from service.Request_Bid import Request_Bid
from user.Address import Address
from user.Billing import Billing
from user.Client import Client
from user.Professional import Professional
from user.User_Question import User_Question


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
        if isinstance(obj, user.User.User):
            return user.User.User.ToAPI(obj)

        elif isinstance(obj, Address):
            return Address.ToAPI(obj)

        elif isinstance(obj, Billing):
            return Billing.ToAPI(obj)

        elif isinstance(obj, Client):
            return Client.ToAPI(obj)

        elif isinstance(obj, Professional):
            return Professional.ToAPI(obj)

        elif isinstance(obj, User_Question):
            return User_Question.ToAPI(obj)

        elif isinstance(obj, Request):
            return Request.ToAPI(obj)

        elif isinstance(obj, Request_Bid):
            return Request_Bid.ToAPI(obj)

        raise TypeError
