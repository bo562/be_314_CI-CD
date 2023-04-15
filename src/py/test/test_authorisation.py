import unittest
from security.Authorisation import Authorisation
from util.database.Database import Database
from util.database.DatabaseLookups import DatabaseLookups


class MyTestCase(unittest.TestCase):
    def test_validate_credentials(self):
        result = Authorisation.validate_credentials('jbondthe21th@outlook.com', 'Password1')
        print(result)

    def test_security_controller(self):
        user_id = 195
        database = Database.database_handler(DatabaseLookups.User)

        database.select(('authorisation_id', 'refresh_token', 'number_of_uses', 'invalidated', 'user_id'),
                        'authorisation')
        database.where('user_id = %s', user_id)
        database.ampersand('invalidated = %s', 'N')

        print(database.run())


if __name__ == '__main__':
    unittest.main()
