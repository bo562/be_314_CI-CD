"""
py that describes the controller for the user sub-package. Enabling User creation, manipulation and
authentication/authorisation
The controller should mimic the functionality of expected output of Lambda function in AWS
"""
from types import SimpleNamespace
from mysql.connector.errors import Error
from util.database import Database
from datetime import datetime
import json
from user.User import User
from user.Address import Address
from user.Subscription import Subscription
from user.Client import Client
from user.Professional import Professional
from user.Billing import Billing
from user.User_Question import User_Question


class User_Controller:
    __event: str  # actual data sent from api gateway
    __context: object

    def __init__(self, event: str):
        self.__event = event
        self.__context = json.loads(event['context'])

    @staticmethod
    def Event_Start(event: str, context: str):
        # create controller to handle event
        user_controller = User_Controller(event=event, context=context)

        # begin handling event
        user_controller.handle_event()

    def handle_event(self):
        result = None  # store result to return to requester

        # determine which method to call based on api request
        if self.__context['resource-path'] == '/user/userCreate':
            self.create_user()

        elif '/user/updateUser' in self.__context['resource-path']:  # since the path will contain the user id
            self.update_user()

    def create_user(self) -> User:
        pass

    def update_user(self) -> User:
        pass
