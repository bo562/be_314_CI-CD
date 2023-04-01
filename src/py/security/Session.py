"""
py that describes the session object, with supporting functions
"""
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Session:
    session_id: int
    access_token: str = None
    expiry_date: datetime = None
    authorisation_id: int = None
