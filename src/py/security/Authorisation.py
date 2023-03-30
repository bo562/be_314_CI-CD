"""
py that describes authorisation object with supporting functions
"""


class Authorisation:
    def __init__(self, authorisation_id, refresh_token, numberof_uses, invalidated, user_id):
        self.authorisation_id: int = authorisation_id
        self.refresh_token: str = refresh_token
        self.numberof_uses: int = numberof_uses
        self.invalidated: bool = invalidated
        self.user_id: int = user_id
