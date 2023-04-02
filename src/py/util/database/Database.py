from mysql.connector.locales.eng import client_error  # for compilation, no real use in code
from mysql.connector.errors import Error
from mysql.connector import errorcode, MySQLConnection, connect
from botocore.exceptions import ClientError
from util.database.DatabaseStatus import DatabaseStatus
import boto3
import json


class Database:
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
        self.database_disconnect()

    @staticmethod
    def database_handler(secret_name):
        # retrieve secret from aws
        try:
            secret = Database.get_secret(secret_name)
            mysql_info = json.loads(secret)
        except Exception as e:
            raise e

        # attempt database connection
        try:
            database = Database(mysql_info['host'], mysql_info['database'],
                                mysql_info['username'], mysql_info['password'])
        except Error as err:
            raise err

        return database

    @staticmethod
    def get_secret(secret_name):
        region_name = "us-east-1"

        # create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        # secret response
        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            raise e

        # decrypts secret using the associated KMS key.
        secret = get_secret_value_response['SecretString']

        return secret

    def database_connect(self):
        if not self.__database_connection.is_connected():
            self.__database_connection.connect()
            self.status = DatabaseStatus.Connected

    def database_disconnect(self):
        if self.__database_connection.is_connected():
            self.__database_connection.close()
            self.__database_connection.disconnect()
        self.status = DatabaseStatus.Disconnected

    def database_query(self, query, args: tuple = None):
        cursor = self.__database_connection.cursor()
        try:
            # attempt to run query and return results
            cursor.execute(query, args)
            result = cursor.fetchall()
        except Error as err:
            raise err

        return result
