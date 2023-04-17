"""
Main py file that handles all inputs/outputs for the /serviceRequest endpoint.
Supports the /serviceRequest endpoint of the API.
This is what the service lambda will use to run the majority of code
"""
from service.Service_Controller import Service_Controller


def service_handler(event, context):
    result = Service_Controller.Event_Start(event=event)

    return result
