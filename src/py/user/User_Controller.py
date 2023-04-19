"""
py that describes the controller for the user sub-package. Enabling User creation, manipulation and
authentication/authorisation
The controller should mimic the functionality of expected output of Lambda function in AWS
"""

import json
import user
from util.handling.Result_Handler import Result_Handler
from util.handling.errors.database.DatabaseObjectAlreadyExists import DatabaseObjectAlreadyExists
from util.handling.errors.database.FailedToCreateDatabaseObject import FailedToCreateDatabaseObject
from util.handling.errors.database.FailedToUpdateDatabaseObject import FailedToUpdateDatabaseObject
from util.packager.Decoder import Decoder


class User_Controller:
    __event: dict  # actual data sent from api gateway
    __context = None

    def __init__(self, event: dict):
        self.__event = event
        self.__context = event.get('context')

    @staticmethod
    def Event_Start(event: dict):
        # create controller to handle event
        user_controller = User_Controller(event=event)

        # begin handling event
        return user_controller.handle_event()

    def handle_event(self):
        # determine which method to call based on api request
        if self.__context.get('resource-path') == '/user/userCreate':
            return self.create_user()

        elif '/user/updateUser' in self.__context.get('resource-path'):  # since the path will contain the user id
            return self.update_user()

        elif self.__context.get('resource-path') == '/user/validate':
            return self.validate_user()

        elif self.__context.get('resource-path') == '/user/userGet':
            return self.get_user()

    def create_user(self) -> object:
        try:
            json_body = self.__event.get('body-json')
            usr = Decoder(json.dumps(json_body), ).deserialize()
            new_user = usr.create_user()

        except FailedToCreateDatabaseObject as fcdo:
            return fcdo.generate_api_error()

        except DatabaseObjectAlreadyExists as doae:
            return doae.generate_api_error()

        return Result_Handler.Prepare_For_API('200', new_user)

    def update_user(self) -> user.User:
        try:
            json_body = self.__event.get('body-json')
            usr = Decoder(json.dumps(json_body)).deserialize()
            updated_user = usr.update_user()

        except DatabaseObjectAlreadyExists as doae:
            return doae.generate_api_error()

        except FailedToUpdateDatabaseObject as fudo:
            return fudo.generate_api_error()

        return Result_Handler.Prepare_For_API('200', updated_user)

    def validate_user(self) -> dict:
        return user.User.User.validate_email(self.__context.get('email_address'))

    def get_user(self) -> dict:
        usr = user.User.User.get_user(self.__context.get('user_id'))
        return Result_Handler.Prepare_For_API('200', usr)
