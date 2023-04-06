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
    Billing: [] = None

    # SQL query to create user in User table
    def create_user(self, first_name: str, last_name: str, email_address: str, mobile: str, password: str):
        pass

    # SQL query to update a field in User Table
    def update_detail(self, attribute: str, value):
        pass

    # return user object (possibly in json form)
    def get_user(self, obj):
        pass

    def get_in_billing(self, ):
        for bill in self.Billing:
            if bill.billing_type == 'In':
                return bill

        return None

    def get_out_billing(self, ):
        for bill in self.Billing:
            if bill.billing_type == 'Out':
                return bill

        return None

    # customer return type for defined API
    @staticmethod
    def default(obj):
        if isinstance(obj, User):
            remap = {
                "userID": obj.user_id,
                "firstname": obj.first_name,
                "lastname": obj.last_name,
                "email": obj.email_address,
                "password": obj.password,
                "mobile": obj.mobile,
                "address": obj.address,
                "client": obj.client,
                "professional": obj.professional,
                "CCout": obj.get_out_billing()
            }
            return remap

        raise TypeError
