"""
py that describes the security question object with supporting functions
"""
from datetime import datetime


class Security_Question:
    def __init__(self, security_question_id, question, retired):
        self.security_question_id: int = security_question_id
        self.question: str = question
        self.retired: datetime = retired
