"""
py that describes the controller for the service sub-package. Enabling...
"""


class Service_Controller:
    __event: str  # actual data sent from api gateway
    __context = None

    def __init__(self, event: str):
        self.__event = event
        self.__context = event.get('context')

    def create_request(self):
        pass

    def update_request(self):
        pass

    def get_request(self):
        pass

    def create_transaction(self):
        pass

    def update_transaction(self):
        pass

    def get_transaction(self):
        pass