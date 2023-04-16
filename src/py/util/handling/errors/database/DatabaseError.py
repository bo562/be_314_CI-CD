"""
py that describes abstract expection for all database errors
"""
from util.handling.errors.API_Exception import API_Exception


class DatabaseError(API_Exception):
    __table: str
    __query: str

    def __init__(self, status_code: str, table: str, query: str, message: str):
        self.__table = table
        self.__query = query
        super().__init__(status_code, message)  # call parent constructor
