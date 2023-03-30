"""
class for address data structure
"""


class address:
    def __init__(self, address_id, street_number, street_name, suburb, postcode, state, user_id):
        self.address_id: int = address_id
        self.street_number: int = street_number
        self.street_name: str = street_name
        self.suburb: str = suburb
        self.postcode: int = postcode
        self.state: str = state
        self.user_id: int = user_id
