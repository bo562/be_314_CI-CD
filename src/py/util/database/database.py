from mysql.connector.locales.eng import client_error # for compilation, no real use in code
from mysql.connector.errors import Error
from mysql.connector import errorcode, MySQLConnection, connect
from botocore.exceptions import ClientError
from util.database.DatabaseStatus import DatabaseStatus
import boto3
import json


class Database():
    def __init__(self, host, database, user, password):
        self.status: DatabaseStatus = NotImplemented

        # creating mysql connection
        self.database_connection = MySQLConnection(user=user, password=password, host=host, database='LambdaTest')

        # check database connection status
        if self.database_connection.is_connected():
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
            database = Database(mysql_info['host'], 'Project',
                                mysql_info['username'], mysql_info['password'])
            database.database_connect()
        except Error as err:
            return err

        return database

    @staticmethod
    def get_secret(secret_name):
        region_name = "us-east-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        # Decrypts secret using the associated KMS key.
        secret = get_secret_value_response['SecretString']

        return secret

    def database_connect(self):
        if not self.database_connection.is_connected():
            self.database_connection.connect()
            self.status = DatabaseStatus.Connected

    def database_disconnect(self):
        if self.database_connection.is_connected():
            self.database_connection.disconnect()
            self.database_connection.close()
        self.status = DatabaseStatus.Disconnected

    def database_select(self, table):
        pass

    def database_insert(self, row):
        pass

    def database_update(self):
        pass

    def database_delete(self):
        pass

    def database_query(self, query):
        cursor = self.database_connection.cursor()
        try:
            cursor.execute(query)
        except Error as err:
            raise err

        print(cursor.fetchall())