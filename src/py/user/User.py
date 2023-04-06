"""
Class file for user data type
"""
from dataclasses import dataclass
from user import Professional as P, Client as C, Address as A, Billing as B


@dataclass
class User:
    user_id: int = None
    first_name: str = None
    last_name: str = None
    email_address: str = None  # doubles as username
    mobile: str = None
    address: A.Address = None
    password: str = None  # will be hashed
    client: C.Client = None  # possibly null
    professional: P.Professional = None  # possibly null
    Billing: [B.Billing] = None

    # SQL query to create user in User table
    def create_user(self, first_name: str, last_name: str, email_address: str, mobile: str, password: str):
        pass

    # SQL query to update a field in User Table
    def update_detail(self, attribute: str, value):
        pass

    # return user object (possibly in json form)
    def get_user(self):
        pass