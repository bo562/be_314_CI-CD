"""
py that utlises orjson to package DTO classes for return to Front-End and deserialse JSONs from FRONT end
for manipulation in database
"""

import orjson
from user.User import User
from user.Address import Address
from user.Billing import Billing


class Packager:
    __object: object

    def __init__(self, obj: object):
        self.__object = obj

    def serialize(self) -> bytes:
        return orjson.dumps(self.__object,
                            option=orjson.OPT_PASSTHROUGH_DATACLASS,
                            default=Packager.default)

    def deserialize(self):
        pass

    # based on object type call correct default method
    @staticmethod
    def default(obj: object):
        if isinstance(obj, User):
            return User.default(obj)

        elif isinstance(obj, Address):
            return Address.default(obj)

        elif isinstance(obj, Billing):
            return Billing.default(obj)

        raise TypeError
