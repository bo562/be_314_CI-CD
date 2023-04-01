"""
py class for credit card data structure
"""
from datetime import datetime


class Billing:
    billing_id: int
    name: str = None
    card_number: int = None
    expiry_date: datetime = None
    cvv: int = None
    billing_type: str = None
