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

    def delete_professional(self):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)
        database.clear()

        database.delete('professional')
        database.where('professional_id = %s', self.professional_id)

        try:
            database.run()
            database.commit()
        except Exception as e:
            return False

        return True

    def retrieve_services(self):
        # connect to database
        database = Database.database_handler(DatabaseLookups.User)

        # create database query
        database.clear()
        database.select(('service_id',), 'associated_service')
        database.where('professional_id = %s', self.professional_id)

        # run query
        try:
            results = database.run()
        except Exception as e:
            raise e

        services = []
        for provided_service in results:
            services.append(Service.get_by_service_id(provided_service[0]))

        self.services = services

    def get_service_names(self) -> [str]:
        services = []
        for service in self.services:
            services.append(service.service_name)

        return services

    @staticmethod
    def get_professional(user_id: int):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # get user object
        database.clear()
        database.select(('professional_id', 'subscription_id', 'user_id'), 'professional')
        database.where('user_id = %s', user_id)

        # try to get authorisation
        professional = None
        try:
            results = database.run()

        except Exception as e:
            raise e

        if len(results) > 0:  # i.e something is returned
            professional = Professional(professional_id=results[0][0], subscription_id=results[0][1],
                                        user_id=results[0][2])

            # get services
            professional.retrieve_services()

        return professional

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Professional):
            remap = {
                "services": obj.services,
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

        return Professional(services=obj.get('services'), CCin=obj.get('CCIn'), subscription_id=subscription_id)
