"""
py that describes the class that handles all results returned from classes and other controllers
Will handle all encoding and structuring of responses to be returned to user and API gateway, making it simpler for the
gatway to set generate the correct status codes
"""
from util.packager.Encoder import Encoder
import json


class Result_Handler:
    @staticmethod
    def Prepare_For_API(status_code: str, result: object):
        to_return = dict()
        to_return['statusCode'] = status_code
        to_return.update(json.loads(Encoder(result).serialize().decode('utf-8')))  # .decode converts from bytes to string

        return to_return

    # when trying to fix parsing error use this method
    @staticmethod
    def no_status_code(result: object):
        return json.loads(Encoder(result).serialize().decode('utf-8'))
