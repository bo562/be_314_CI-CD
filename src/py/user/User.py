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
            self.user_id = database.run()[0]
            return self

        # add nested classes
        database.clear()
        self.ccout.create_billing(self.user_id)
        self.address.create_address(self.user_id)

        # conditional nesting (may not occur for all users)
        if self.client is not None:
            self.client.create_client(self.user_id)

        if self.professional is not None:
            self.professional.create_professional(self.user_id)

        # commit and close database connection
        database.disconnect()

        return self

    def update_user(self):
        try:
            database = Database.database_handler(DatabaseLookups.User.value)  # create database to connect to
            database.database_connect()  # connect to database
            query = "SELECT user_id FROM project.user WHERE user_id=%d"
            query_data = self.user_id
            validation_check = database.database_query(query, query_data)
            if not isinstance(validation_check, int) or validation_check < 0:
                return "invalid id"
        except Exception as e:
            print("Database Connection Error")
        query = ("UPDATE project.user "
                 "firstname = %s, lastname = %s, email_address = %s, mobile = %s, password = %s "
                 "WHERE user_id = %d")
        query_data = (self.firstname, self.lastname, self.email_address, self.mobile, self.password, self.user_id)
        database.database_query(query, query_data)
        query = "SELECT user_id FROM project.user WHERE email_address=%s"
        query_data = self.email_address
        tuser_id = database.database_query(query, query_data)
        if not isinstance(tuser_id, int) or tuser_id < 0:
            return "User update Failed"
        self.user_id = tuser_id
        database.database_disconnect()

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
