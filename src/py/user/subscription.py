"""
py that handles subscription information
"""
from datetime import datetime


class Subscription:
    def __init__(self, subscription_id, subscription_name, fee, start_date, end_date):
        self.subscription_id: int = subscription_id
        self.subscription_name: str = subscription_name
        self.fee: float = fee
        self.start_date: datetime = start_date
        self.end_date: datetime = end_date
