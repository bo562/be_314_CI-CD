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
    __event: str  # actual data sent from api gateway
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

    def login(self):
        user_id = Authorisation.validate_credentials(self.__context.get('email_address'),
                                                     self.__context.get('password'))

        # check if login worked
        if user_id is None: return {"statusCode": "Email or Password Incorrect"}

        # check for authorisation that is not invalided else create a new authorsation
        authorisation = Authorisation()
        authorisation = authorisation.get_authorisation(user_id=user_id)

        # if no authorisation was found for user
        if authorisation is None:
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

        encoded = Encoder(user).serialize()

        to_return = {
            "access_token": session.access_token,
            "refresh_token": authorisation.refresh_token,
            "expiry": session.expiry_date.__str__(),
            "user": json.loads(encoded)  # due to the way that AWS stringify responses
        }

        return to_return
