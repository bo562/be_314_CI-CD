"""
py file that contains all information about the review object and functions supporting object
"""
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Review:
    review_id: int
    review_date: datetime = None
    rating: float = None
    comment: str = None
    request_id: int = None

    def create_review(self, review_date: datetime, rating: float, comment: str, request_id: int):
        pass

    def update_review(self, review_id: int, review_date: datetime, rating: float, comment: str, request_id: int):
        pass

    def get_review(self):
        pass
