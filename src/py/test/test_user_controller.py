import unittest

from user.User_Controller import User_Controller


class MyTestCase(unittest.TestCase):
    def test_controller(self):
        user_input = """
        {
            "body-json": {
                "user_id": 1,
                "firstName": "James",
                "lastName": "Bond",
                "email": "jbond@outlook.com",
                "mobile": "0412345678",
                "password": "Password1",
                "address": {
                    "streetNumber": "8",
                    "streetName": "Biggie Street",
                    "suburb": "Liverpool",
                    "postcode": "2170"
                },
                "CCOut": {
                    "CCName": "Outgoing",
                    "CCNumber": "1234 5678 9111 2134",
                    "CVV": "123",
                    "billingType": "Out",
                    "expiryDate": "11/2024"
                },
                "client": {
                    "membershipType": "Subscription"
                },
                "professional": {
                    "CCin": {
                        "CCName": "Incoming",
                        "CCNumber": "4444 4444 4444 4444",
                        "CVV": "333",
                        "billingType": "In",
                        "expiryDate": "11/2025"
                    },
                    "services": [
                        "Oven Repairs",
                        "Fence Installation",
                        "Roof Cleaning"
                    ]
                },
                "securityQuestions": {
                    "securityQuestion1": {
                        "securityQuestion": "What was your first car?",
                        "answer": "Car"
                    },
                    "securityQuestion2": {
                        "securityQuestion": "What was your childhood nickname?",
                        "answer": "Nickname"
                    },
                    "securityQuestion3": {
                        "securityQuestion": "What city were you born in?",
                        "answer": "City"
                    }
                }
            },
            "context": {
                "authorizer-principal-id": "",
                "caller": "",
                "http-method": "POST",
                "stage": "dev",
                "request-id": "9a48d040-e44a-40c3-9b6a-f6ea2ac1a766",
                "resource-id": "k2axvw",
                "resource-path": "/user/userCreate"
            }
        }
        """

        result = User_Controller.Event_Start(user_input)
        print(result)


if __name__ == '__main__':
    unittest.main()
