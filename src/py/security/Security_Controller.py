"""
py that describes controller for security
handling generating tokens, verifying tokens etc.
"""

import json
from security.Authorisation import Authorisation
from security.Session import Session
from user.Subscription import Subscription
from user.User import User
from util.packager.Decoder import Decoder
from util.packager.Encoder import Encoder
from datetime import datetime, timedelta


class Security_Controller:
    __event: dict  # actual data sent from api gateway
    __context = None

    def __init__(self, event: str):
        self.__event = event
        self.__context = event.get('context')

    @staticmethod
    def Event_Start(event: str):
        # create controller to handle event
        user_controller = Security_Controller(event=event)

        # begin handling event
        return user_controller.handle_event()

    def handle_event(self):
        # determine which method to call based on api request
        if self.__context.get('resource-path') == '/user/login':
            return self.login()

        elif self.__context.get('resource-path') == '/user/resetPassword':
            # handle different methods triggered at endpoint
            if self.__context.get('http-method') == 'GET':
                return self.get_user_questions()

            elif self.__context.get('http-method') == 'POST':
                return self.validate_user_questions()

            elif self.__context.get('http-method') == 'PUT':
                return self.update_password()

        elif self.__event.get('type') is not None:
            return self.__event

        else:
            return {
                "statusCode": "403",
                "message": "No existing endpoint {}".format(self.__event.get('resource-path'))
            }

    def login(self):
        # use prebuilt function to handle validation and return user_id
        user_id = Authorisation.validate_credentials(self.__context.get('email_address'),
                                                     self.__context.get('password'))

        # check if validation returned user
        if user_id is None:
            return {
                "statusCode": "404",
                "message": "Email or Password Incorrect"
            }

        # check for authorisation that is not invalided else create a new authorisation
        authorisation = None
        with Authorisation.get_authorisation(user_id) as authorisation:
            # if no authorisation was found for user
            if authorisation.get_authorisation(user_id=user_id) is None:
                authorisation = Authorisation(refresh_token=Authorisation.generate_refresh_token(user_id=user_id))
                authorisation = authorisation.create_authorisation(user_id=user_id)

        # generate session for user
        expiry_date = datetime.now() + timedelta(days=1)
        access_token = Session.generate_access_token(authorisation.refresh_token)
        session = Session(expiry_date=expiry_date, access_token=access_token,
                          authorisation_id=authorisation.authorisation_id)
        session = session.create_session(authorisation_id=authorisation.authorisation_id)

        # get user
        user = User.get_user(user_id=user_id)

        # serialize json to deserialze in dict for AWS Stringify
        encoded = Encoder(user).serialize()
        to_return = {
            "statusCode": "200",
            "access_token": session.access_token,
            "refresh_token": authorisation.refresh_token,
            "expiry": session.expiry_date.__str__(),
            "user": json.loads(encoded)  # due to the way that AWS stringify responses
        }

        return to_return

    # to authorize actions on protected endpoints
    def Authorize_Event(self):
        session_id = Session.validate_session(self.__event.get('authorizationToken'))

        if session_id is None:
            return {
                "statusCode": "403",
                "message": "Unauthorized"
            }

        else:
            return {
                "statusCode": "202",
                "message": "Token Accepted"
            }

    # for step one of resetPassword
    def get_user_questions(self):
        user_id = User.get_user_id(self.__context.get('email_address'))

        # check if user was returned from validation
        if user_id is None:
            return {
                "statusCode": "404",
                "message": "User not found"
            }

        # create user object and iterate through questions
        user = User.get_user(user_id)
        questions = []
        for question in user.security_questions:
            questions.append(question.ToAPI(question))  # utilising already created ToAPI Method

        # return information
        to_return = {
            "statusCode": "200",
            "user_id": user_id,
            "questions": questions
        }

        return to_return

    def validate_user_questions(self):
        pass

    def update_password(self):
        pass
