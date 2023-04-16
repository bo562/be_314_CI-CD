"""
py that describes the class that handles all results returned from classes and other controllers
Will handle all encoding and structuring of responses to be returned to user and API gateway, making it simpler for the
gatway to set generate the correct status codes
"""
from util.packager.Encoder import Encoder


class Result_Handler:
    @staticmethod
    def Prepare_For_API(status_code: str, result: object):
        return {
            "statusCode": status_code,
            "result": Encoder(result).serialize()
        }