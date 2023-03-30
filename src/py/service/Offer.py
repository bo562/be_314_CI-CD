"""
py that holds all details regarding Offer
"""
from datetime import datetime


class Offer:
    def __init__(self, offer_id, date_sent, client_accepted, professional_accepted, request_offer_status, professional_id):
        self.offer_id: int = offer_id
        self.date_sent: datetime = date_sent
        self.client_accepted: bool = client_accepted
        self.professional_accepted: bool = professional_accepted,
        self.request_offer_status: str = request_offer_status,
        self.professional_id: int = professional_id
