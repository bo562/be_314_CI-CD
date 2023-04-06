"""
py class for client data structure
"""
from dataclasses import dataclass
from util.database import Database as db, DatabaseLookups as dl


@dataclass
class User_Question:
    user_question_id: int = None
    user_id: int = None
    answer: str = None
    security_question_id: int = None

    def create_question(self, user_id: int, security_question: str):
        try:
            database = db.Database.database_handler(dl.DatabaseLookups.user.value)  # create database to connect to
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
        query = ("INSERT INTO project.user_question "
                 "(user_id, security_question_id, answer) "
                 "VALUES (%d, %d, %s)")
        query_data = (user_id, self.security_question_id, self.answer)
        database.database_query(query, query_data)
        query = "SELECT user_question_id FROM project.user_question WHERE user_id=%d AND security_question_id=%d"
        query_data = (user_id, self.security_question_id)
        temp_user_question_id = database.database_query(query, query_data)
        if temp_user_question_id is None:
            return "Security Question creation failed"
        self.clint_id = temp_user_question_id
        database.database_disconnect()

    def update_question(self, user_id: int, security_question: str):
        try:
            database = db.Database.database_handler(dl.DatabaseLookups.user.value)  # create database to connect to
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

    def get_question(self):
        try:
            database = db.Database.database_handler(dl.DatabaseLookups.user.value)  # create database to connect to
            database.database_connect()  # connect to database
        except Exception as e:
            print("Database Connection Error")
        query = "SELECT question FROM project.security_question WHERE security_question_id=%d"
        query_data = (self.security_question_id)
        return database.database_query(query, query_data)
        database.database_disconnect()
