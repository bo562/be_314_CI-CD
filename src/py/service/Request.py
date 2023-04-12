"""
py that handles data for requests type
"""
from datetime import datetime
from dataclasses import dataclass


@dataclass()
class Request:
    request_id: int
    request_date: datetime = None
    start_date: datetime = None
    completion_date: datetime = None
    instruction: str = None
    client_id: int = None
    professional_id: int = None
    service_id: int = None

    def create_request(self):
        pass

    def update_request(self):
        pass

    def get_request(self):
        pass