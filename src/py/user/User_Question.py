"""
py that describes the security question answers object, with supporting functionality
"""
import json
from dataclasses import dataclass


@dataclass
class User_Question:
    user_question_id: int
    user_id: int = None
    security_question_id: int = None
    answer: str = None

    @staticmethod
    def FromAPI(obj):
        security_questions = []
        for val in obj:
            security_questions.append(User_Question(obj[val]['securityQuestion'], obj[val]['answer']))
        return security_questions
