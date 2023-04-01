"""
class for address data structure
"""
from dataclasses import dataclass


@dataclass
class Address:
    address_id: int
    street_number: int = None
    street_name: str = None
    suburb: str = None
    postcode: int = None
    state: str = None
