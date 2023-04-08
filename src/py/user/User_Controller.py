"""
py that describes the controller for the user sub-package. Enabling User creation, manipulation and
authentication/authorisation
The controller should mimic the functionality of expected output of Lambda function in AWS
"""

import json
from user.User import User


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

        return "Hello Lambda!"

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
