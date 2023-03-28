"""
Class file for user data type
"""

from user import professional as p
from user import client as c

class User:
    def __init__(self, user_id, firstname, lastname, email_address, mobile,
                 address_id, password, client: c.Client, professional: p.Professional):
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.email_address = email_address  # doubles as username
        self.mobile = mobile
        self.address_id = address_id
        self.password = password  # will be hashed
        self.client = client  # possibly null
        self.professional = professional  # possibly null

# function that takes in a json and returns a User instance
    def createUserFromJson(self, json: str):
        pass