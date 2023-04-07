"""
Class file for user data type
"""
import json
from dataclasses import dataclass

from user.Address import Address
from user.Client import Client
from user.Professional import Professional
from user.Billing import Billing


@dataclass
class User:
    user_id: int = None
    first_name: str = None
    last_name: str = None
    email_address: str = None  # doubles as username
    mobile: str = None
    address: Address = None
    password: str = None  # will be hashed
    client: Client = None  # possibly null
    professional: Professional = None  # possibly null
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
    def ToAPI(obj):
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

    @staticmethod
    def FromAPI(obj):
        # create base user object
        usr = User(user_id=obj.get('userID'), first_name=obj.get('firstname'), last_name=obj.get('lastname'),
                   email_address=obj.get('email'), address=obj.get('address'), password=obj.get('password'))

        return usr
