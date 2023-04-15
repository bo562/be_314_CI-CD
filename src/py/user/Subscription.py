"""
py that handles subscription information
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Subscription:
    subscription_id: int
    subscription_name: str = None
    fee: float = None


