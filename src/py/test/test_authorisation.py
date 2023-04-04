"""
Unit tests for Authorisation functions
"""

from security.Authorisation import Authorisation
from user.User import User

auth = Authorisation()

auth.create_authorisation("jtest@gmail.com", "asdqwdww@@@")

