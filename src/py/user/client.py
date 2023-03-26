"""
py class for client data structure
"""


class Client:
    def __init__(self, client_id, subscription_id, user_id):
        self.client_id = client_id
        self.subscription_id = subscription_id
        self.user_id = user_id