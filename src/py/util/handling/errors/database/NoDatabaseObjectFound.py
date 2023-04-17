"""
py that describes the error when object does not exists in the database
"""
from util.handling.errors.database.DatabaseError import DatabaseError


class NoDatabaseObjectFound(DatabaseError):
    def __init__(self, table: str, query: str, database_object: object,
                 status_code: str = '400', message='Database object does not exist'):
        self.__database_object = database_object
        super().__init__(status_code=status_code, table=table, query=query, database_object=database_object,
                         message=message)