"""
py that describes when creation of user fails
"""
from util.handling.errors.database.DatabaseError import DatabaseError


class FailedToCreateUser(DatabaseError):
    """When system fails to create a user for any reason"""
    __object: object

    def __init__(self, status_code: str, table: str, query: str, message: str):
        super().__init__(status_code, table, query, message)  # call parent constructor
