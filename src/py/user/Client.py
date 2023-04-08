"""
py class for client data structure
"""
from dataclasses import dataclass


@dataclass
class Client:
    client_id: int
    subscription_id: int = None

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Client):
            remap = {
                "membershiptype": obj.subscription_id
            }
            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        return Client(client_id=-1, subscription_id=obj.get('membershipType'))
