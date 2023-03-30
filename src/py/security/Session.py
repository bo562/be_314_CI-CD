"""
py that describes the session object, with supporting functions
"""
from datetime import datetime


class Session:
    def __init__(self, session_id, access_token, expiry_date, authorisation_id):
        self.session_id: int = session_id
        self.access_token: str = access_token
        self.expiry_date: datetime = expiry_date
        self.authorisation_id: int = authorisation_id
