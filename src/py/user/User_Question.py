"""
py class for client data structure
"""
from dataclasses import dataclass
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseStatus import DatabaseStatus
from mysql.connector import errors
from security.Security_Question import Security_Question


@dataclass
class User_Question:
    user_question_id: int = None
    user_id: int = None
    answer: str = None
    security_question_id: int = None

    def create_question(self, user_id: int):
        database = Database.database_handler(DatabaseLookups.User)  # create database instance

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # if user_id is null
        if self.user_id is None:
            self.user_id = user_id

        # insert question into database
        database.clear()
        database.insert(self, 'user_question', ('user_question_id',))

        try:
            self.user_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:  # in case that user already exists
            if ie.errno == 1452:  # cannot solve gracefully
                database.disconnect()
                raise ie

            # constructing query to return already created user
            database.clear()
            database.select(('user_id',), 'user_question')
            database.where('user_id = %s', self.user_id)

            # run query and return user_id
            self.user_id = database.run()[0][0]
            return self

        # commit and close database connection
        database.disconnect()

        return self

    def update_question(self, user_id: int, security_question: str):
        try:
            database = Database.database_handler(DatabaseLookups.user.value)  # create database to connect to
            database.database_connect()  # connect to database
            query = "SELECT user_id FROM project.user WHERE user_id=%d"
            query_data = (user_id)
            validationcheck = database.database_query(query, query_data)
            if not isinstance(validationcheck, int) or validationcheck < 0:
                return "invalid id"
        except Exception as e:
            print("Database Connection Error")
        query = "SELECT security_question_id FROM project.security_question WHERE question=%s"
        query_data = (security_question)
        temp_security_question_id = database.database_query(query, query_data)
        if temp_security_question_id is None:
            return "security question doesnt exist"
        self.security_question_id = temp_security_question_id
        query = ("UPDATE project.user_question "
                 "SET user_id = %d, security_question_id = %d, answer = %s "
                 "WHERE user_id =%d")
        query_data = (user_id, self.security_question_id, self.answer, user_id)
        database.database_query(query, query_data)
        query = "SELECT user_question_id FROM project.user_question WHERE user_id=%d AND security_question_id=%d"
        query_data = (user_id, self.security_question_id)
        temp_user_question_id = database.database_query(query, query_data)
        if temp_user_question_id is None:
            return "Security Question creation failed"
        self.user_question_id = temp_user_question_id
        database.database_disconnect()

    def delete_security_question(self):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()

        database.delete('user_question')
        database.where('user_question_id = %s', self.security_question_id)

        try:
            database.run()
        except Exception as e:
            return False

        return True

    def get_question(self):
        try:
            database = Database.database_handler(DatabaseLookups.user.value)  # create database to connect to
            database.database_connect()  # connect to database
        except Exception as e:
            print("Database Connection Error")
        query = "SELECT question FROM project.security_question WHERE security_question_id=%d"
        query_data = (self.security_question_id)
        return database.database_query(query, query_data)
        database.database_disconnect()

    @staticmethod
    def FromAPI(obj):
        security_questions = []
        for val in obj:
            print()
            security_question = Security_Question.get_by_answer(obj[val].get('securityQuestion'))
            security_questions.append(User_Question(security_question_id=security_question.security_question_id,
                                                    answer=obj[val].get('answer')))
        return security_questions
