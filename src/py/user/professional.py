"""
py class for professional data structure
"""


class Professional:
    def __init__(self, professional_id, subscription_id, user_id):
        self.professional_id: int = professional_id
        self.subscription_id: int = subscription_id
        self.user_id: int = user_id
