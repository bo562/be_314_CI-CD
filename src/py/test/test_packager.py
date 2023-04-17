import orjson

from service.Request import Request
from user.User import User
from user.Address import Address
from user.Billing import Billing
from user.Client import Client
from user.Professional import Professional
from user.Subscription import Subscription
from user.User_Question import User_Question
from service.Service import Service
from util.packager.Encoder import Encoder
from util.packager.Decoder import Decoder
import unittest


class TestPackager(unittest.TestCase):
    def test_serialize(self):
        address = Address(address_id=1, street_number='10', street_name='Adam Street', suburb='James Park',
                          postcode='3434')
        billing_in = Billing(billing_id=1, name='David James', card_number='1234 4567 8910 1112',
                             expiry_date='10/2024', ccv='123', billing_type='In')
        billing_out = Billing(billing_id=1, name='David James', card_number='2111 0198 1233 3323',
                              expiry_date='10/2025', ccv='123', billing_type='Out')
        client = Client(subscription_id=1)
        services = [
            Service(service_id=1, service_name='Tree Removal'),
            Service(service_id=2, service_name='Oven Repairs')
        ]
        professional = Professional(user_id=1, professional_id=2, subscription_id=1,
                                    services=services, CCin=billing_in)
        security_questions = [
            User_Question(user_question_id=None, user_id=147, answer="Cat", security_question_id=1),
            User_Question(user_question_id=None, user_id=147, answer="Cat", security_question_id=1)
        ]
        usr = User(user_id=1, first_name='James', last_name='Bond', email_address='jbond@gmail.com',
                   mobile='04102342342', address=address, password='password', client=client, professional=professional,
                   ccout=billing_out, security_questions=security_questions)

        packager = Encoder(usr)
        print(packager.serialize())

    def test_deserialize(self):
        user_input = """
            {
                "user_id": 1,
                "firstName": "James",
                "lastName": "Bond",
                "email": "jbond@outlook.com",
                "password": "Password1",
                "mobile": "0412345678",
                "CCOut": {
                    "CCName": "Outgoing",
                    "CCNumber": "1234 5678 9111 2134",
                    "expiryDate": "11/2024",
                    "CCV": "123",
                    "billingType": "Out"
                },
                "address": {
                    "streetname": "Biggie Street",
                    "streetnumber": "8",
                    "suburb": "Liverpool",
                    "postcode": "2170"
                },
                "client": {
                    "membershipType": "Subscription"
                },
                "professional": {
                    "services": [
                        "Oven Repairs",
                        "Fence Installation",
                        "Roof Cleaning"
                    ],
                    "CCIn": {
                        "CCName": "Incoming",
                        "CCNumber": "4444 4444 4444 4444",
                        "expiryDate": "11/2025",
                        "CCV": "333",
                        "billingType": "In"
                    }
                },
                "securityQuestions": [
                    {
                        "securityQuestion": "What was your first car?",
                        "answer": "Car"
                    },
                    {
                        "securityQuestion": "What was your childhood nickname?",
                        "answer": "Nickname"
                    },
                    {
                        "securityQuestion": "What city were you born in?",
                        "answer": "City"
                    }
                ]                                    
            }
        """

        decoder = Decoder(user_input, User)
        result = decoder.deserialize()
        print(result)

    def test_request_unpacking(self):
        request = """{
            "requestID": 0,
            "requestDate": "10/12/2023",
            "serviceType": "Plumbing",
            "requestStatus": "New",
            "jobDescription": "My Toilet is broken",
            "clientID": "10",
            "professionalID": "1"
        }"""

        decoded = Decoder(request).deserialize()
        print(decoded)

    def test_request_packing(self):
        request = Request(request_id=None, request_date='10/12/2023', start_date=None, completion_date=None,
                          instruction='My Toilet is broken', client_id=7, professional_id=3, service_id=4,
                          request_status_id=1)

        encoded = Encoder(request).serialize()
        print(encoded)

    def test_request_bid_packing(self):
        request_bid = """ {
            "requestID": 0,
            "applicationID": 0,
            "offerDate": "string",
            "userID": 1,
            "cost": 0,
            "applicationStatus": "string"
        }
        """

        encoded = Encoder(request_bid).serialize()
        print(encoded)

    if __name__ == '__main__':
        unittest.main(warnings='ignore')
