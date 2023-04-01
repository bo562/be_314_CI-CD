"""
py class for professional data structure
"""
from dataclasses import dataclass


@dataclass
class Professional:
    professional_id: int
    subscription_id: int = None
    user_id: int = None
