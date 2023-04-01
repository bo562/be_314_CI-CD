"""
py file that describes the Service object and functions supporting it
"""
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Service:
    service_id: int
    service: str = None
    cost: float = None
    retired: datetime = None

    def create_service(self, service: str, cost: float, retired: datetime):
        pass

    def update_service(self, service_id: int, service: str, cost: float, retired: datetime):
        pass

    def get_service(self):
        pass
