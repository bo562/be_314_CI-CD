"""
class for address data structure
"""


class address:
    def __init__(self, street_number, street_name, suburb, postcode, state, user_id):
        self.street_number = street_number
        self.street_name = street_name
        self.suburb = suburb
        self.postcode = postcode
        self.state = state
        self.user_id = user_id