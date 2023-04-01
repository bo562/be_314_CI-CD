"""
py that describes authorisation object with supporting functions
"""
from dataclasses import dataclass


@dataclass
class Authorisation:
    authorisation_id: int
    refresh_token: str = None
    numberof_uses: int = None
    invalidated: bool = None
    user_id: int = None
