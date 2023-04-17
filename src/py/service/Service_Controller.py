"""
py that describes the controller for the service sub-package. Enabling...
"""
import json

from util.handling.Result_Handler import Result_Handler
from util.handling.errors.database.DatabaseConnectionError import DatabaseConnectionError
from util.handling.errors.database.DatabaseObjectAlreadyExists import DatabaseObjectAlreadyExists
from util.handling.errors.database.FailedToCreateDatabaseObject import FailedToCreateDatabaseObject
from util.packager.Decoder import Decoder


class Service_Controller:
    __event: dict  # actual data sent from api gateway
    __context = None

    def __init__(self, event: dict):
        self.__event = event
        self.__context = event.get('context')

    @staticmethod
    def Event_Start(event: dict):
        # create controller to handle event
        service_controller = Service_Controller(event=event)

        # begin handling event
        return service_controller.handle_event()

    def handle_event(self):
        # determine which method to call based on api request
        if self.__context.get('resource-path') == '/serviceRequest':
            # handle different methods triggered at endpoint
            if self.__context.get('http-method') == 'GET':
                return self.__event

            elif self.__context.get('http-method') == 'POST':
                return self.client_create_request()

            elif self.__context.get('http-method') == 'PUT':
                return self.client_update_request()

    def client_create_request(self):
        json_body = self.__event.get('body-json')
        service_request = Decoder(json.dumps(json_body)).deserialize()

        try:
            new_service_request = service_request.create_request()

        except DatabaseConnectionError as dce:
            return dce.generate_api_error()

        except DatabaseObjectAlreadyExists as doae:
            return doae.generate_api_error()

        except FailedToCreateDatabaseObject as fcdo:
            return fcdo.generate_api_error()

        return Result_Handler.Prepare_For_API('200', new_service_request)

    def client_update_request(self):
        pass
