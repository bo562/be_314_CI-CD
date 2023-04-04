"""
py that describes the session object, with supporting functions
"""
from datetime import datetime
from dataclasses import dataclass
from hashlib import sha256


@dataclass
class Session:
    session_id: int
    access_token: str = None
    expiry_date: datetime = None
    authorisation_id: int = None

    @staticmethod
    def generate_access_token(refresh_token: str):
        to_hash = refresh_token + datetime.datetime.now().strftime("%d/%m/%YT%H:%M:%S")
        hashed = sha256(to_hash.encode('utf-8')).hexdigest()

        return hashed
