"""
py that describes the error when there is some programming error
"""
from util.handling.errors.database.DatabaseError import DatabaseError


class DatabaseProgrammingError(DatabaseError):
    def __init__(self, table: str, query: str, database_object: object,
                 status_code: str = '500', message='Programming Error'):
        self.__database_object = database_object
        super().__init__(status_code=status_code, table=table, query=query, database_object=database_object,
                         message=message)
