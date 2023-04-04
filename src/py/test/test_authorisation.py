"""
Unit tests for Authorisation functions
"""

from security.Authorisation import Authorisation
from user.User import User

usr = User(-1)
auth = Authorisation.generate_token(usr)