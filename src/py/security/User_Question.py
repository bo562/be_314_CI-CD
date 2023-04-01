"""
py that describes the security question answers object, with supporting functionality
"""
from dataclasses import dataclass


@dataclass
class User_Question:
    user_question_id: int
    user_id: int = None
    security_question_id: int = None
    answer: str = None
