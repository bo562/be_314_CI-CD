"""
Class file for user data type
"""

from user import professional as p, client as c, address as a

class User:
    def __init__(self, user_id, firstname, lastname, email_address, mobile,
                 address_id, password, client_id, professional_id):
        self.user_id: int = user_id
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.email_address: str = email_address  # doubles as username
        self.mobile: str = mobile
        self.address: int = address_id
        self.password: str = password  # will be hashed
        self.client: int = client_id  # possibly null
        self.professional: int = professional_id  # possibly null

# function that takes in a json and returns a User instance
    def CreateUserFromJson(self, json):
        pass