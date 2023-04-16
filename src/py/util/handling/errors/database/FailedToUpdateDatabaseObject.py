"""
py that describes the error when system fails to update a specific object in the database
"""
from util.handling.errors.database.DatabaseError import DatabaseError


class FailedToUpdateDatabaseObject(DatabaseError):
    __database_object: object

    def __init__(self, status_code: str, table: str, query: str, database_object: object,
                 message='Failed to update database object'):
        self.__database_object = database_object
        super().__init__(status_code=status_code, table=table, query=query, database_object=database_object,
                         message=message)
