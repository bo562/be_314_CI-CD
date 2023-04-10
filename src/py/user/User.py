"""
Class file for user data type
"""
from dataclasses import dataclass
from mysql.connector import errors
from user.User_Question import User_Question
from user.Address import Address
from user.Client import Client
from user.Professional import Professional
from user.Billing import Billing
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseStatus import DatabaseStatus
import json


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
    ccout: Billing = None
    security_questions: [User_Question] = None

    # SQL query to create user in User table
    def create_user(self) -> 'User':
        database = Database.database_handler(DatabaseLookups.User)  # create database instance

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # attempt to create base user
        database.clear()
        database.insert(self, 'user', ('user_id', 'address', 'ccout', 'client', 'professional', 'security_questions'))

        try:
            self.user_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:  # in case that user already exists
            if ie.errno == 1452:  # cannot solve gracefully
                database.disconnect()
                raise ie

            # constructing query to return already created user
            database.clear()
            database.select(('user_id', ), 'user')
            database.where('email_address = %s', self.email_address)

            # run query and return user_id
            self.user_id = database.run()[0][0]
            return self

        # add nested classes
        database.clear()
        self.ccout.create_billing(self.user_id)
        self.address.create_address(self.user_id)

        # due to multiple questions, need to loop and call
        for security_question in self.security_questions:
            security_question.create_question(self.user_id)

        # conditional nesting (may not occur for all users)
        if self.client is not None:
            self.client.create_client(self.user_id)

        if self.professional is not None:
            self.professional.create_professional(self.user_id)

        # commit and close database connection
        database.disconnect()

        return self

    def update_user(self):
        database = Database.database_handler(DatabaseLookups.User)  # create database instance

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # attempt to create base user
        database.clear()
        database.update(self, 'user', ('user_id', 'address', 'ccout', 'client', 'professional', 'security_questions'))
        database.where('user_id = %s', self.user_id)

        # run database query and commit
        try:
            database.run()
            database.commit()

        except errors.IntegrityError as ie:  # in case that user already exists
            raise ie

        except Exception as e:  # other unhandled exceptions
            raise e

        # conditional nesting (may not occur for all user updates)
        if self.ccout is not None:
            self.ccout.update_billing(self.user_id)

        if self.address is not None:
            self.address.update_address(self.user_id)

        if self.client is not None:
            self.client.update_client(self.user_id)

        if self.professional is not None:
            self.professional.update_professional(self.user_id)

        # commit and close database connection
        database.disconnect()

        return self

    # return user object (possibly in json form)
    def get_user(self, obj):
        pass

    @staticmethod
    def validate_email(email):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)

        # create database query
        database.clear()
        database.select(('user_id',), 'user')
        database.where('email_address = %s', email)

        # get results and check if user exists
        results = database.run()
        if len(results) > 0:
            return {
                "exists": "True",
                "pbkey": "MIGbMBAGByqGSM49AgEGBSuBBAAjA4GGAAQBihRpdJQxhxfvRCsPLUUdtQ5FayRLVs9wIYhdoYzs0eey3xE1WLrOfzjNa"
                         "YB6wsrs2dCBu3PC8sxeTMEe92w8NP0AO4wHu471c4Rtf5JUjVgg5Nu+/n5Npus32UjqaXhbNVIDEOHKpSZKpJh2cKRqfG"
                         "OuSbiW/Z+WdvOILMoMiPuImQo="
            }
        elif len(results) == 0:
            return {"exists": "False"}
        else:
            return {"exists": "Not Working"}

    # customer return type for defined API
    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, User):
            remap = {
                "user_id": obj.user_id,
                "firstName": obj.first_name,
                "lastName": obj.last_name,
                "email": obj.email_address,
                "password": obj.password,
                "mobile": obj.mobile,
                "address": obj.address,
                "client": obj.client,
                "professional": obj.professional,
                "CCout": obj.ccout
            }
            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        # create base user object
        usr = User(user_id=obj.get('user_id'), first_name=obj.get('firstName'), last_name=obj.get('lastName'),
                   email_address=obj.get('email'), address=obj.get('address'), mobile=obj.get('mobile'),
                   ccout=obj.get('CCOut'), password=obj.get('password'), client=obj.get('client'),
                   security_questions=obj.get('securityQuestions'), professional=obj.get('professional'))

        return usr
