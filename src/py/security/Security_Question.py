"""
py that describes the security question object with supporting functions
"""
from datetime import datetime
from dataclasses import dataclass
from util.database.Database import Database
from util.database.DatabaseStatus import DatabaseStatus
from util.database.DatabaseLookups import DatabaseLookups

@dataclass
class Security_Question:
    security_question_id: int
    question: str = None
    retired: datetime = None

    @staticmethod
    def get_by_answer(question):
        # connect to database
        database = Database.database_handler(DatabaseLookups.User)

        print(question)

        # create database query
        database.clear()
        database.select(('security_question_id', 'question', 'retired'), 'security_question')
        database.where('question = %s', question)

        # run query
        try:
            results = database.run()
        except Exception as e:
            raise e
        print(results)
        return Security_Question(security_question_id=results[0][0], question=results[0][1], retired=results[0][2])
