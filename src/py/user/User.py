"""
Class file for user data type
"""
from dataclasses import dataclass

from user.User_Question import User_Question
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
    Billing: Billing = None
    Security_Questions: [User_Question] = None

    # SQL query to create user in User table
    def create_user(self, first_name: str, last_name: str, email_address: str, mobile: str, password: str):
        pass

    # SQL query to update a field in User Table
    def update_detail(self, attribute: str, value):
        pass

    # return user object (possibly in json form)
    def get_user(self, obj):
        pass

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
                "CCout": obj.Billing
            }
            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        # create base user object
        usr = User(user_id=obj.get('user_id'), first_name=obj.get('firstName'), last_name=obj.get('lastName'),
                   email_address=obj.get('email'), address=obj.get('address'), mobile=obj.get('mobile'),
                   Billing=obj.get('CCOut'), password=obj.get('password'), client=obj.get('client'),
                   Security_Questions=obj.get('securityQuestions'), professional=obj.get('professional'))

        return usr
