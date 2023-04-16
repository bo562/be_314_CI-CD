"""
Class file for user data type
"""
from dataclasses import dataclass
from mysql.connector import errors
from security.Security_Question import Security_Question
from user.User_Question import User_Question
from user.Address import Address
from user.Client import Client
from user.Professional import Professional
from user.Billing import Billing
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseStatus import DatabaseStatus
from util.handling.errors.database.DatabaseObjectAlreadyExists import DatabaseObjectAlreadyExists
from util.handling.errors.database.DatabaseProgrammingError import DatabaseProgrammingError
from util.handling.errors.database.FailedToCreateDatabaseObject import FailedToCreateDatabaseObject
from util.handling.errors.database.FailedToUpdateDatabaseObject import FailedToUpdateDatabaseObject


@dataclass
class User:
    user_id: int = None
    first_name: str = None
    last_name: str = None
    email_address: str = None  # doubles as username
    mobile: str = None
    address: Address = None
    password: str = None  # will be hashed
    client: Client = None  # possibly null
    professional: Professional = None  # possibly null
    ccout: Billing = None
    security_questions: ['User_Question'] = None

    # SQL query to create user in User table
    def create_user(self) -> 'User':
        database = Database.database_handler(DatabaseLookups.User)  # create database instance

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # attempt to create base user
        database.insert(self, 'user', ('user_id', 'address', 'ccout', 'client', 'professional', 'security_questions'))

        try:
            self.user_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:  # in case that user already exists
            query = database.review_query()  # retrieve query

            # clean up instance
            database.rollback()
            database.clear()
            database.disconnect()

            if ie.errno == 1452:  # cannot solve gracefully
                # raise error
                raise DatabaseObjectAlreadyExists(table='user', query=query, database_object=self)

            raise FailedToCreateDatabaseObject(table='user', query=query, database_object=self)

        # add nested classes
        # attempt to create billing object
        try:
            self.ccout = self.ccout.create_billing(self.user_id)

        except DatabaseObjectAlreadyExists as doae:
            self.delete_user()  # abort creation of user object
            raise doae

        except FailedToCreateDatabaseObject as fcdo:
            self.delete_user()
            raise fcdo

        # attempt to create address object
        try:
            self.address = self.address.create_address(self.user_id)

        except DatabaseObjectAlreadyExists as doae:
            self.delete_user()  # abort creation of user object
            raise doae

        except FailedToCreateDatabaseObject as fcdo:
            self.delete_user()
            raise fcdo

        # due to multiple questions, need to loop and call
        security_questions = []
        for security_question in self.security_questions:
            result = security_question.create_question(self.user_id)
            security_questions.append(result)
            if result is None:
                self.delete_user()
                raise Exception(f'User Creation Failed Due to Security Questions')

        # conditional nesting (may not occur for all users)
        if self.client is not None:
            self.client = self.client.create_client(self.user_id)

            if self.client is None:
                self.delete_user()
                raise Exception(f'User Creation Failed Due to Address')

        if self.professional is not None:
            self.professional.create_professional(self.user_id)

            if self.professional is None:
                self.delete_user()
                raise Exception(f'User Creation Failed Due to Professional')

        # commit and close database connection
        database.disconnect()

        return self.get_user(self.user_id)

    def update_user(self):
        database = Database.database_handler(DatabaseLookups.User)  # create database instance

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # only if the base fields are not empty run updates on user table
        if self.check_empty() is False:
            # attempt to update base user
            database.update(self, 'user', ('user_id', 'address', 'ccout', 'client', 'professional', 'security_questions'))
            database.where('user_id = %s', self.user_id)

            # run database query and commit
            try:
                database.run()
                database.commit()

            except errors.IntegrityError as ie:  # in case that change violates consistency constraints
                database.rollback()
                query = database.review_query()
                database.clear()
                database.disconnect()

                # if there is an integrity error
                if ie.errno == 1452:  # cannot solve gracefully
                    # raise error
                    raise DatabaseObjectAlreadyExists(table='user', query=query, database_object=self)

                # some other consistency constraint check
                raise FailedToUpdateDatabaseObject(table='user', query=query, database_object=self)

            except errors.ProgrammingError as e:  # due to no columns being updated
                database.rollback()
                query = database.review_query()
                database.clear()
                database.disconnect()

                raise DatabaseProgrammingError(table='user', query=query, database_object=self)

        # conditional nesting (may not occur for all user updates)
        if self.ccout is not None and type(self.ccout) != dict:
            self.ccout.update_billing(self.user_id)

        if self.address is not None and type(self.address) != dict:
            self.address.update_address(self.user_id)

        if self.client is not None and type(self.client) != dict:
            # check if client previously existed
            client = Client.get_client(self.user_id)

            # if client exists update, else create the client
            if client is None:
                self.client = self.client.create_client(self.user_id)
            else:
                self.client.update_client(self.user_id)

            self.client.update_client(self.user_id)

        if self.professional is not None and type(self.professional) != dict:
            # check if professional previously existed
            professional = Professional.get_professional(self.user_id)

            # if client exists update, else create the professional
            if professional is None:
                self.professional = self.professional.create_professional(self.user_id)
            else:
                self.professional.update_professional(self.user_id)

        # commit and close database connection
        database.clear()
        database.disconnect()

        return self.get_user(self.user_id)

    # delete entire user object
    def delete_user(self) -> None:
        # delete nested objects first
        try:
            if self.ccout is not None: self.ccout.delete_billing()
            if self.address is not None: self.address.delete_address()
            if self.client is not None: self.client.delete_client()
            if self.professional is not None: self.professional.delete_professional()
            if len(self.security_questions) != 0:
                for security_question in self.security_questions:
                    security_question.delete_security_question()

        except Exception as e:  # something has really gone wrong and is not fixable
            raise e

        # create database connection
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()

        database.delete('user')
        database.where('user_id = %s', self.user_id)

        try:
            database.run()
            database.commit()

        except Exception as e:
            database.rollback()
            raise e

    # validate user_question
    def validate_answer(self, question: str, answer) -> bool:
        # iterate through user questions and check if an answer does not match
        passed = False
        for user_question in self.security_questions:
            if Security_Question.get_by_id(user_question.security_question_id).question == question:
                if answer == user_question.answer:
                    passed = True
                    break

        return passed

    # check if all base fields are null
    def check_empty(self) -> bool:
        count = 0

        # add 1 to count if all the fields are none
        if self.user_id is None: count += 5
        if self.first_name is None: count += 1
        if self.last_name is None: count += 1
        if self.email_address is None: count += 1
        if self.mobile is None: count += 1
        if self.password is None: count += 1

        # if count is 5 then object is empty, if count is less than 5 then okay to run queries
        return True if count >= 5 else False

    # return user object (possibly in json form)
    @staticmethod
    def get_user(user_id: int):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # get user object
        database.select(('user_id', 'first_name', 'last_name', 'email_address', 'mobile', 'password'), 'user')
        database.where('user_id = %s', user_id)

        # try to get authorisation
        user = None
        try:
            results = database.run()

        except Exception as e:
            raise e

        if len(results) > 0:
            user = User(user_id=results[0][0], first_name=results[0][1], last_name=results[0][2],
                        email_address=results[0][3], mobile=results[0][4], password=results[0][5],
                        address=Address.get_address(user_id), client=Client.get_client(user_id),
                        professional=Professional.get_professional(user_id),
                        security_questions=User_Question.get_by_user_id(user_id))

        return user

    # did not update get_user due to dependencies
    @staticmethod
    def get_user_id(email_address: str):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # get user object
        database.select(('user_id',), 'user')
        database.where('email_address = %s', email_address)

        # run database query
        try:
            result = database.run()

        except Exception as e:
            raise e

        if len(result) != 0:
            return result[0][0]

        else:
            return None

    @staticmethod
    def validate_email(email):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)

        # create database query
        database.select(('user_id',), 'user')
        database.where('email_address = %s', email)

        # get results and check if user exists
        results = database.run()
        if len(results) > 0:
            return {"exists": "True"}
        elif len(results) == 0:
            return {
                "exists": "False",
                "pbkey": "MIICCgKCAgEAxlpvDY1SbHbF+JYO0xSvSXCdOeLiqmTTO9k3FJF6Y7RE9Icwh4q4"
                         "z7ReQyP05OMB902QjCjzXlvC9prMGj4luRoSfbVOk9Ia5kcO5FEeNt7Xvy0aNSpn"
                         "EtuwTHumykJDxrTKzOfyR7o7HJM6mGXmA5kS8k/FiPYwSCaewtmt8XlgWxSUWyDo"
                         "lAe4SuLxyRg4vLpMVCxW/rGgqrNq78vKWeFZBeXnvNHP/cqApUB3Cu3Q5VcF5sq/"
                         "vUOe3NkilM9e9BSr963/GVsFyg6wL+guAlUPxpNhQY9HTye2BxJQ/DZZFxN9rCaO"
                         "//ZsUUVCg5k7Z+NjtcKAep82KbwvkGtqAQ+UFSLB8jgOMvX+mfJesAfItfKV52pF"
                         "Bit/qzKT40KMgWLvDene2d/Ug2HFjK+hX8ikh6S9kIMEwcGPCw4hBd/MK92S/jK2"
                         "Oy2ZkA29jAclCvq9kh9geaQRMTnIEsvnLmsgEadMgXYAC5VUdTRYYZ6vZffNAbsR"
                         "0mEvUD9zcCa3KF6c9G0bXjwbZJ0HUn8DKVgnpueXCd9457K7Gst/lwEtlXiY17yD"
                         "MaVMYtmgmyTzdKmXb643akkYzp2vGlYyK5kRAbiMRqE2xlxRATn76+da9mvpV517"
                         "lXqCUVC4VUUZDIdOTmptOzpSzGgcowriJVU5TgbQOS//s87GKH+fCqcCAwEAAQ=="
            }
        else:
            return {"exists": "Not Working"}

    # customer return type for defined API
    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, User):
            remap = {
                "user_id": obj.user_id,
                "firstName": obj.first_name,
                "lastName": obj.last_name,
                "email": obj.email_address,
                "password": obj.password,
                "mobile": obj.mobile,
                "address": obj.address,
                "client": None if obj.client is None else obj.client,
                "professional": None if obj.professional is None else obj.professional,
                "securityQuestions": obj.security_questions
            }
            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        # create base user object
        usr = User(user_id=obj.get('user_id'), first_name=obj.get('firstName'), last_name=obj.get('lastName'),
                   email_address=obj.get('email'), address=obj.get('address'), mobile=obj.get('mobile'),
                   ccout=obj.get('CCOut'), password=obj.get('password'), client=obj.get('client'),
                   security_questions=obj.get('securityQuestions'), professional=obj.get('professional'))

        return usr
