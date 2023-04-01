"""
py class for client data structure
"""
from dataclasses import dataclass


@dataclass
class Client:
    client_id: int
    subscription_id: int = None
