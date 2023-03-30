"""
py file that contains all information about the review object and functions supporting object
"""
from datetime import datetime


class Review:
    def __init__(self, review_id, review_date, rating, comment, request_id):
        self.review_id: int = review_id
        self.review_date: datetime = review_date
        self.rating: float = rating
        self.comment: str = comment
        self.request_id: int = request_id
