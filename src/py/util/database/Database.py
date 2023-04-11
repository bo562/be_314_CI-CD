from typing import List

from mysql.connector.locales.eng import client_error  # for compilation, no real use in code
from mysql.connector.errors import Error
from mysql.connector import errorcode, MySQLConnection, connect
from botocore.exceptions import ClientError
from util.database.DatabaseStatus import DatabaseStatus
from util.database.DatabaseAction import DatabaseAction
from util.database.DatabaseSymbol import DatabaseSymbol
import boto3
import json


class Database:
    __database_connection: MySQLConnection
    __table: str = None
    __columns: [] = []
    __data: [] = []
    __current_action: DatabaseAction
    __query: str = ""
    __cursor = None

    def __init__(self, host, database, user, password):
        self.status: DatabaseStatus = NotImplemented

        # creating mysql connection
        self.__database_connection = MySQLConnection(user=user, password=password, host=host, database=database)

        # check database connection status
        if self.__database_connection.is_connected():
            self.status = DatabaseStatus.Connected
        else:
            self.status = DatabaseStatus.Disconnected

    def __del__(self):
        self.disconnect()

    @staticmethod
    def database_handler(secret_name):
        # retrieve secret from aws
        """ # issues with aws
        try:
            secret = Database.get_secret(secret_name)
            mysql_info = json.loads(secret)
        except Exception as e:
            raise e
        """

        # attempt database connection
        try:
            database = Database('csit314-gp.crjrzvrrbory.us-east-1.rds.amazonaws.com', 'Project',
                                'user_lambda', 'uDb+J5Jr7vV)ek>')
        except Error as err:
            raise err

        return database

    @staticmethod
    def get_secret(secret_name: DatabaseStatus):
        region_name = "us-east-1"

        # create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        # secret response
        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name.value)
        except ClientError as e:
            raise e

        # decrypts secret using the associated KMS key.
        secret = get_secret_value_response['SecretString']

        return secret

    def connect(self):
        if not self.__database_connection.is_connected():
            self.__database_connection.connect()
            self.status = DatabaseStatus.Connected

    def disconnect(self):
        if self.__database_connection.is_connected():
            self.__database_connection.close()
            self.__database_connection.disconnect()
        self.status = DatabaseStatus.Disconnected

    # query types
    def select(self, columns: tuple, table: str):
        # clear previous query
        self.clear()

        # set variables
        self.__table = table
        self.__current_action = DatabaseAction.SELECT
        self.__query = 'SELECT {} FROM {} '  # store query for database interaction

        # collect information from data_object for selection
        to_select = ''
        if type(columns) is tuple:
            to_select = ",".join(columns)

        else:
            to_select = columns

        self.__query = self.__query.format(to_select, table)

    def insert(self, data_object: object, table: str, ignore: tuple = ()):
        # clear previous query
        self.clear()

        # set variables
        self.__table = table
        self.__current_action = DatabaseAction.INSERT
        self.__query = 'INSERT INTO {} ({}) VALUES ({})'  # store query for database interaction

        # collect information from data_object for selection
        to_insert = ''
        strings = []  # for inserting data into query

        keys = data_object.__dict__.items()
        for item in keys:
            if item[1] is not None and item[0] not in ignore:
                self.__columns.append(item[0])
                self.__data.append(item[1])
                strings.append('%s')

        to_insert = ",".join(self.__columns)
        inserting = ",".join(strings)

        self.__query = self.__query.format(table, to_insert, inserting)

    def update(self, data_object: object, table: str, ignore: tuple = ()):
        # clear previous query
        self.clear()

        # set variables
        self.__table = table
        self.__current_action = DatabaseAction.UPDATE
        self.__query = 'UPDATE {} SET {}'  # store query for database interaction

        # collect information from data_object for selection
        strings = []  # for inserting data into query

        # iterate through fields in object and store information
        keys = data_object.__dict__.items()
        for item in keys:
            if item[1] is not None and item[0] not in ignore:
                self.__columns.append(item[0])
                self.__data.append(item[1])
                strings.append('%s')

        # create set portion of query
        to_update = '=%s,'.join(self.__columns)
        to_update += '=%s '  # join will not add the last argument

        self.__query = self.__query.format(table, to_update)

    def delete(self, table: str):
        # clear previous query
        self.clear()

        # set variables
        self.__table = table
        self.__current_action = DatabaseAction.DELETE
        self.__query = 'DELETE FROM {} '.format(table)  # store query for database interaction

    def query(self, query: str, args: tuple = (), return_id: bool = False):
        # set variables
        self.__query = query
        self.__data = args

        self.__cursor = self.__database_connection.cursor()
        try:
            self.__cursor.execute(query, args)
        except Error as err:  # simple error handling
            self.clear()
            raise err
        else:
            if return_id is True:
                return self.__cursor.getlastrowid()
            else:
                return self.__cursor.fetchall()

    # query augmenting
    def where(self, clause: str, value: str):
        self.__query += "WHERE " + clause + " "  # extra space for adding more queries
        self.__data.append(value)

    def ampersand(self, clause: str, value: str):
        self.__query += 'AND ' + clause + ' '  # extra space for adding more queries
        self.__data.append(value)

    def bar(self, clause: str, value: str):
        self.__query += 'OR ' + clause + ' '  # extra space for adding more queries
        self.__data.append(value)

    # query actions
    def review_query(self):
        return self.__query

    def inner_join(self, table: str, left: str, right: str):
        self.__query += 'INNER JOIN {} ON {} = {} '.format(table, left, right)

    def left_join(self, table: str, left: str, right: str):
        self.__query += 'LEFT JOIN {} ON {} = {} '.format(table, left, right)

    def right_join(self, table: str, left: str, right: str):
        self.__query += 'RIGHT JOIN {} ON {} = {} '.format(table, left, right)

    def run(self):
        # create cursor for querying
        self.__cursor = self.__database_connection.cursor()

        # query database using created query
        try:
            # switch between different actions, as they require different returns
            if self.__current_action is DatabaseAction.SELECT:  # if query is select
                # check if there are any params for example in where
                if len(self.__data) > 0:
                    return self.query(self.__query, self.__data)
                else:
                    return self.query(self.__query)

            # all other queries should return row id
            else:
                result = self.query(self.__query, self.__data, return_id=True)
                return result

        except Error as err:  # simple error handling if works return true otherwise return false
            raise err

    def commit(self):
        self.__database_connection.commit()

    def clear(self):
        self.__table: str = None
        self.__columns.clear()
        self.__data.clear()
        self.__query: str = ""

        # close cursor
        if self.__cursor is not None:
            self.__cursor.close()
            self.__cursor = None
