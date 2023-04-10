"""
py class for professional data structure
"""
from dataclasses import dataclass
from mysql.connector import errors
from service.Service import Service
from service.Associated_Service import Associated_Service
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

        # add associated services for professional
        if self.services is not None:
            for service in self.services:
                # get service object
                service_object = Service.get_by_service_name(service_name=service)

                # create associated_service object to push to database
                associated_service = Associated_Service(professional_id=self.professional_id,
                                                        service_id=service_object.service_id)

                # create association
                associated_service.create_associated_service(self.professional_id)

        # clear database tool
        database.clear()

        return self

    def update_professional(self, user_id: int):
        database = Database.database_handler(DatabaseLookups.User)  # create database connection

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        elif database.status is DatabaseStatus.NoImplemented:
            raise errors.InternalError  # change with mysql errors

        # attempt to create billing object
        if self.user_id is None:
            self.user_id = user_id

        # create query
        database.clear()
        database.update(self, 'professional', ('professional_id', 'services', 'CCin'))
        database.where('user_id = %s', self.user_id)

        try:  # attempt to return
            self.professional_id = database.run()
            database.commit()

        except errors.IntegrityError as ie:
            raise ie

        # clear database tool
        database.clear()

        return self

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
        # get subscription_id from 'Subscription' value (could change ids in the future)
        subscription_name = 'Subscription'
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()
        database.select(('subscription_id',), 'subscription')
        database.where('subscription_name = %s', subscription_name)
        results = database.run()
        subscription_id = results[0][0] if results is not None else None

        return Professional(services=obj.get('services'), CCin=obj.get('CCin'), subscription_id=subscription_id)
