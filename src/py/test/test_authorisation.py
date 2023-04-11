import unittest
from security.Authorisation import Authorisation


class MyTestCase(unittest.TestCase):
    def test_validate_credentials(self):
        self.assertEqual(180, Authorisation.validate_credentials('jbondthe10th@outlook.com', 'Password1'))  # add assertion here


if __name__ == '__main__':
    unittest.main()
