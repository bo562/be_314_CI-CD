import json
import unittest

from service.Request import Request
from util.handling.Result_Handler import Result_Handler
from util.packager.Encoder import Encoder


class MyTestCase(unittest.TestCase):
    def test_create_request(self):
        request = Request(request_date='10/12/2023', service_id=1, postcode='2570',
                          request_status_id=1, instruction="Test", client_id=1)

        print(request.create_request())

    def test_get_request(self):
        print(Request.get_request(6))

    def test_update_request(self):
        request = Request(request_id=6, instruction="Testing this change")
        updated_request = request.update_request()
        print(updated_request)

    def test_get_by_client_id(self):
        requests = Request.get_client_requests(1)
        encoded = Encoder(requests).serialize()
        print(json.loads(Encoder(requests).serialize().decode('utf-8')))

    def test_get_request_postcode(self):
        print(Request.get_by_postcode(2570))


if __name__ == '__main__':
    unittest.main()
