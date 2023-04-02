"""
py that holds all details regarding Offer
"""
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Offer:
    offer_id: int
    date_sent: datetime = None
    client_accepted: bool = None
    professional_accepted: bool = None,
    request_offer_status: str = None,
    professional_id: int = None

    def create_offer(self, date_sent: datetime, client_accepted: bool, professional_accepted: bool,
                     request_offer_status: str, professional_id: int):
        pass

    def update_offer(self, offer_id: int, date_sent: datetime, client_accepted: bool, professional_accepted: bool,
                     request_offer_status: str, professional_id: int):
        pass

    def get_transaction(self):
        pass