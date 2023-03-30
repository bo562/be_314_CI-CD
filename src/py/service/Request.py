"""
py that handles data for requests type
"""
from datetime import datetime


class Request:
    def __init__(self, request_id, request_date, start_date, completion_date, instruction, client_id, professional_id, service_id):
        self.request_id: int = request_id
        self.request_date: datetime = request_date
        self.start_date: datetime = start_date
        self.completion_date: datetime = completion_date
        self.instruction: str = instruction
        self.client_id: int = client_id
        self.professional_id: int = professional_id
        self.service_id: int = service_id
