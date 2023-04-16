"""
py file that describes the Service object and functions supporting it
"""
from datetime import datetime
from dataclasses import dataclass
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups


@dataclass
class Service:
    service_id: int
    service_name: str = None
    cost: float = None
    retired: datetime = None

    def create_service(self, service_name: str, cost: float, retired: datetime):
        pass

    def update_service(self, service_id: int, service_name: str, cost: float, retired: datetime):
        pass

    @staticmethod
    def get_by_service_id(service_id: int) -> 'Service':
        # connect to database
        database = Database.database_handler(DatabaseLookups.User)

        # create database query
        database.select(('service_id', 'service_name', 'cost', 'retired'), 'service')
        database.where('service_id = %s', service_id)

        # run query
        try:
            results = database.run()
        except Exception as e:
            # clean up and disconnect
            database.clear()
            database.disconnect()
            raise e

        # clear and disconnect from database
        database.clear()
        database.disconnect()

        # return service object from result (some what dangerous if indexing becomes incorrect
        return Service(service_id=results[0][0], service_name=results[0][1], cost=results[0][2], retired=results[0][3])

    @staticmethod
    def get_by_service_name(service_name) -> 'Service':
        # connect to database
        database = Database.database_handler(DatabaseLookups.User)

        # create database query
        database.clear()
        database.select(('service_id', 'service_name', 'cost', 'retired'), 'service')
        database.where('service_name = %s', service_name)

        # run query
        try:
            results = database.run()
        except Exception as e:
            raise e

        return Service(service_id=results[0][0], service_name=results[0][1], cost=results[0][2], retired=results[0][1])
