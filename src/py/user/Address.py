"""
class for address data structure
"""
from dataclasses import dataclass


@dataclass
class Address:
    address_id: int
    street_number: int = None
    street_name: str = None
    suburb: str = None
    postcode: int = None
    state: str = None

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Address):
            remap = {
                "streetname": obj.street_name,
                "streetnumber": obj.street_number,
                "suburb": obj.suburb,
                "postcode": obj.postcode
            }

            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        return Address(address_id=-1, street_number=obj.get('streetNumber'),
                       street_name=obj.get('streetName'), suburb=obj.get('suburb'), postcode=obj.get('postcode'))
