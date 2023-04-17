"""
py that describes the error when system cannot connect to database
"""
from util.handling.errors.database.DatabaseError import DatabaseError


class DatabaseConnectionError(DatabaseError):
    def __init__(self, table: str, query: str, database_object: object,
                 status_code: str = '503', message='Could not connect to database'):
        self.__database_object = database_object
        super().__init__(status_code=status_code, table=table, query=query, database_object=database_object,
                         message=message)
