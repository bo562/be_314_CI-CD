"""
py class for credit card data structure
"""
from datetime import datetime


class Billing:
    def __init__(self, billing_id, name, card_number, expiry_date, cvv, billing_type, user_id):
        self.billing_id: int = billing_id
        self.name: str = name
        self.card_number: int = card_number
        self.expiry_date: datetime = expiry_date
        self.cvv: int = cvv
        self.billing_type: str = billing_type
        self.user_id: int = user_id
