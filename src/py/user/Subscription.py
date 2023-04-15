"""
py that handles subscription information
"""
from dataclasses import dataclass
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups
from util.database.DatabaseStatus import DatabaseStatus


@dataclass
class Subscription:
    subscription_id: int
    subscription_name: str = None
    fee: float = None


    @staticmethod
    def get_subscription(subscription_id: int):
        # create database connection
        database = Database.database_handler(DatabaseLookups.User)

        # check if database is connected, if not connect
        if database.status is DatabaseStatus.Disconnected:
            database.connect()

        # get user object
        database.clear()
        database.select(('subscription_id', 'subscription_name', 'fee'),
                        'subscription')
        database.where('subscription_id = %s', subscription_id)

        # try to get authorisation
        subscription = None
        try:
            results = database.run()

        except Exception as e:
            raise e

        if len(results) > 0:
            subscription = Subscription(subscription_id=results[0][0], subscription_name=results[0][1], fee=results[0][2])

        return subscription

