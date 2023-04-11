"""
Main py file that handles all inputs/outputs for the /user/authorisation endpoints.
Supports the /user endpoint of the API.
This is what the user lambda will use to run the majority of code
"""
from security.Security_Controller import Security_Controller


def security_handler(event, context):
    security_controller = Security_Controller.Event_Start(event=event)

    return security_controller
