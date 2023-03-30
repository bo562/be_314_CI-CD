"""
py that describes the security question answers object, with supporting functionality
"""


class User_Question:
    def __init__(self, user_question_id, user_id, security_question_id, answer):
        self.user_question_id: int = user_question_id
        self.user_id: int = user_id
        self.security_question_id: int = security_question_id
        self.answer: str = answer
