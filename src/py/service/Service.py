"""
py file that describes the Service object and functions supporting it
"""
from datetime import datetime


class Service:
    def __init__(self, service_id, service, cost, retired):
        self.service_id: int = service_id
        self.service: str = service
        self.cost: float = cost
        self.retired: datetime = retired
