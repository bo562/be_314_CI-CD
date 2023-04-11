"""
Main py file that handles all inputs/outputs for the /user endpoint.
Supports the /user endpoint of the API.
This is what the user lambda will use to run the majority of code
"""
from user.User_Controller import User_Controller


def user_handler(event, context):
    user_controller = User_Controller.Event_Start(event=event)

    return user_controller
