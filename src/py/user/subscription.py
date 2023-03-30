'''
py that handles subscription information
'''

class Subscription:
    def __init__(self, subscription_name, fee, start_date, end_date):
        self.subscription_name = subscription_name
        self.fee = fee
        self.start_date = start_date
        self.end_date = end_date