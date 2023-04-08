import unittest
from user.User import User
from user.Billing import Billing
from user.Address import Address


class MyTestCase(unittest.TestCase):
    def test_user_create(self):
        ccout = Billing(billing_id=-1, name='Outgoing', card_number='4444 4444 4444 4444', expiry_date='10/2024',
                        ccv='123', billing_type='Out')
        address = Address(address_id=-1, street_number='10', street_name='Biggie Street', suburb='Liverpool',
                          postcode='2170')
        usr = User(first_name='Jason', last_name='Statham', email_address='jstatham@outlook.com',
                   mobile='9090909090', password='password1', ccout=ccout, address=address)

        creation = usr.create_user()
        print(creation)


if __name__ == '__main__':
    unittest.main()
