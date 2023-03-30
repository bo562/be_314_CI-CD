"""
py that describes transaction object, handles all functionality to do with transactions
"""
from datetime import datetime


class Transaction:
    def __init__(self, transaction_id, cost, transaction_date, transaction_status, user_id, billing_type, billing_id):
        self.transaction_id: int = transaction_id
        self.cost: float = cost
        self.transaction_date: datetime = transaction_date
        self.transaction_status: str = transaction_status
        self.user_id: int = user_id
        self.billing_type: str = billing_type
        self.billing_id: int = billing_id
