"""
py that describes the error when no update fields are provided when updating a row
"""
from util.handling.errors.API_Exception import API_Exception


class NoUpdateFieldsProvided(API_Exception):
    """When passing an object for creation or updating where all the field are empty"""
    def __init__(self, status_code: str, table: str, query: str, message: str):
        super().__init__(status_code, table, query, message)  # call parent constructor
