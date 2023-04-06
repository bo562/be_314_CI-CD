"""
py class for credit card data structure
"""
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Billing:
    billing_id: int
    name: str = None
    card_number: str = None
    expiry_date: str = None
    cvv: str = None
    billing_type: str = None

    @staticmethod
    def default(obj):
        if isinstance(obj, Billing):
            remap = {
                "CCname": obj.name,
                "CCNumber": obj.card_number,
                "expirydate": obj.expiry_date,
                "cvv": obj.cvv,
                "billing_type": obj.billing_type
            }
            return remap

        raise TypeError
