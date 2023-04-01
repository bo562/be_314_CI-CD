"""
py that describes the controller for the user sub-package. Enabling User creation, manipulation and
authentication/authorisation
"""
from types import SimpleNamespace
from util.database import database
import json
from user import User as U


class User_Controller:
    def __init__(self, data: str):
        self.data = data

    def create_user(self, data) -> U.User:
        pass

    def update_user(self, data) -> U.User:
        pass
