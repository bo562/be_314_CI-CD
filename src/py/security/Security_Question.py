"""
py that describes the security question object with supporting functions
"""
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Security_Question:
    security_question_id: int
    question: str = None
    retired: datetime = None
