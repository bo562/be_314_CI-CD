"""
py that describes the controller for the user sub-package. Enabling User creation, manipulation and
authentication/authorisation
The controller should mimic the functionality of expected output of Lambda function in AWS
"""

import json
import traceback
from user.User import User
from util.packager.Decoder import Decoder
from util.packager.Encoder import Encoder


class User_Controller:
    __event: object  # actual data sent from api gateway
    __context = None

    def __init__(self, event: str):
        self.__event = event
        self.__context = event.get('context')

    @staticmethod
    def Event_Start(event: str):
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

    def create_user(self) -> object:
        try:
            json_body = self.__event.get('body-json')
            usr = Decoder(json.dumps(json_body), 'User').deserialize()
            new_user = usr.create_user()

        except Exception as e:
            return {
                "statusCode": "500",
                "error": e.args
            }

        try:
            encoded = Encoder(new_user).serialize()
            return encoded

        except Exception as e:
            return {
                "statusCode": "500",
                "error": e.args
            }

    def update_user(self) -> User:
        try:
            json_body = self.__event.get('body-json')
            usr = Decoder(json.dumps(json_body), User).deserialize()
            updated_user = usr.update_user()

        except Exception as e:
            raise e

        try:
            encoded = Encoder(updated_user).serialize()
            return encoded

        except Exception as e:
            raise e

    def validate_user(self) -> dict:
        return User.validate_email(self.__context.get('email_address'))