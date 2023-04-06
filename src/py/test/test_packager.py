from util.packager.Packager import Packager
from user.User import User
from user.Address import Address
from user.Billing import Billing
import unittest


class TestPackager(unittest.TestCase):
    def test_serialize(self):
        address = Address(address_id=1, street_number=10, street_name='Adam Street', suburb='James Park', postcode=3434)
        billing_in = Billing(billing_id=1, name='David James', card_number='1234 4567 8910 1112', expiry_date='10/2024',
                          cvv='123', billing_type='In')
        billing_out = Billing(billing_id=1, name='David James', card_number='2111 0198 1233 3323', expiry_date='10/2025',
                          cvv='123', billing_type='Out')
        usr = User(user_id=1, first_name='James', last_name='Bond', email_address='jbond@gmail.com',
                   mobile='04102342342', address=address, password='password', Billing=(billing_in,billing_out))

        packager = Packager(usr)
        print(packager.serialize())

    def test_deserialize(self):
        pass

    if __name__ == '__main__':
        unittest.main(warnings='ignore')
