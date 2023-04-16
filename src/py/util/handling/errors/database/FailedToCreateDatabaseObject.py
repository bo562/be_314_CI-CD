"""
py that describes the error when system fails to create a specific object in the database
"""
from util.handling.errors.database.DatabaseError import DatabaseError


class FailedToCreateDatabaseObject(DatabaseError):
    def __init__(self, table: str, query: str, database_object: object,
                 status_code: str = '500', message: str = 'Failed to create database object'):
        self.__database_object = database_object
        super().__init__(status_code=status_code, table=table, query=query, database_object=database_object,
                         message=message)
