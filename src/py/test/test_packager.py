import orjson

from user.User import User
from user.Address import Address
from user.Billing import Billing
from user.Client import Client
from user.Professional import Professional
from user.Subscription import Subscription
from util.packager.Encoder import Encoder
from util.packager.Decoder import Decoder
import unittest


class TestPackager(unittest.TestCase):
    def test_serialize(self):
        address = Address(address_id=1, street_number=10, street_name='Adam Street', suburb='James Park', postcode=3434)
        billing_in = Billing(billing_id=1, name='David James', card_number='1234 4567 8910 1112', expiry_date='10/2024',
                          cvv='123', billing_type='In')
        billing_out = Billing(billing_id=1, name='David James', card_number='2111 0198 1233 3323', expiry_date='10/2025',
                          cvv='123', billing_type='Out')
        client = Client(1, 2)
        professional = Professional(2, 1)
        usr = User(user_id=1, first_name='James', last_name='Bond', email_address='jbond@gmail.com',
                   mobile='04102342342', address=address, password='password', client=client, professional=professional,
                   Billing=billing_out)

        packager = Encoder(usr)
        #print(packager.serialize())

    def test_deserialize(self):
        user_input = """
            {
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
            }
        """

        decoder = Decoder(user_input, User)
        result = decoder.deserialize()
        encoder = Encoder(result)
        print(encoder.serialize())

    if __name__ == '__main__':
        unittest.main(warnings='ignore')
