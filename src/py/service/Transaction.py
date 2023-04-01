"""
py that describes transaction object, handles all functionality to do with transactions
"""
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Transaction:
    transaction_id: int
    cost: float = None
    transaction_date: datetime = None
    transaction_status: str = None
    user_id: int = None
    billing_type: str = None
    billing_id: int = None

    def create_transaction(self, cost: float, transaction_date: datetime, transaction_status: str,
                           user_id: int, billing_type: str, billing_id: int):
        pass

    def update_transaction(self, transaction_id: int, cost: float, transaction_date: datetime, transaction_status: str,
                           user_id: int, billing_type: str, billing_id: int):
        pass

    def get_transaction(self):
        pass
