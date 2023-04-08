"""
py class for professional data structure
"""
from dataclasses import dataclass
from mysql.connector import errors
from service.Service import Service
from user.Billing import Billing
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseStatus import DatabaseStatus


@dataclass
class Professional:
    professional_id: int = None
    subscription_id: int = None
    services: [Service] = None
    CCin: Billing = None
    user_id: int = None

    def create_professional(self, user_id: int):
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise errors.InternalError  # change with mysql errors

        # if user_id null set user_id
        if self.user_id is None:
            self.user_id = user_id

        # attempt to create professional object
        database.insert(self, 'professional', ('professional_id', 'services', 'CCin'))  # create query

        try:
            self.professional_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:
            if ie.errno == 1452:  # cannot solve gracefully
                raise ie

            # get billing data
            database.clear()
            database.select(('professional_id',), 'professional')
            database.where('user_id = %s', self.user_id)

            self.professional_id = database.run()
            return self

        # clear database tool
        database.clear()

        return self

    def update_professional(self, user_id: int):
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
        query = "SELECT subscription_id FROM project.subscription WHERE subscription_type=%s"
        query_data = 'PMembership'
        temp_subscription_id = database.database_query(query, query_data)
        if temp_subscription_id is None:
            return "Membership type doesnt exist"
        self.subscription_id = temp_subscription_id
        query = ("UPDATE project.professional "
                 "SET subscription_id = %d"
                 "WHERE user_id = %d")
        query_data = (self.subscription_id, user_id)
        database.database_query(query, query_data)
        query = "SELECT professional_id FROM project.professional WHERE user_id=%d"
        query_data = (user_id)

        tprofessional_id = database.database_query(query, query_data)
        if tprofessional_id is None:
            return "professional creation failed"
        self.professional_id = tprofessional_id
        database.database_disconnect()

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Professional):
            remap = {
                "services": obj.services,
                "CCin": obj.CCin
            }
            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        return Professional(services=obj.get('services'), CCin=obj.get('CCin'))
