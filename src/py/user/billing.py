"""
py class for credit card data structure
"""


class billing:
    def __init__(self, name, card_number, expiry_date, cvv, billing_type, user_id):
        self.name = name
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.cvv = cvv
        self.billing_type = billing_type
        self.user_id = user_id