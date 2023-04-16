"""
py that describes abstract expection for all database errors
"""
from util.handling.errors.API_Exception import API_Exception


class DatabaseError(API_Exception):
    __table: str
    __query: str
    __database_object: object

    def __init__(self, status_code: str, table: str, query: str, database_object: object,
                 message: str = 'Database Error'):
        self.__table = table
        self.__query = query
        self.__database_object = database_object
        super().__init__(status_code=status_code, message=message)  # call parent constructor

    def generate_api_error(self):
        return {
            "statusCode": self.get_status_code(),
            "errorOnTable": self.__table,
            "errorFromQuery": self.__query
        }
