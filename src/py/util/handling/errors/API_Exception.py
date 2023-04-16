"""
py that houses the class that descirbes the abstract class for handling exceptions to return to API Gateway
"""


class API_Exception(Exception):
    __status_code: str

    def __init__(self, status_code: str, message: str):
        self.__status_code = status_code
        super().__init__(message)

    def get_status_code(self):
        return self.__status_code