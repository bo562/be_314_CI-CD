'''
py that describes transaction object, handles all functionality to do with transactions
'''

class Transaction:
    def __init__(self, Cost, Transaction_Date, Transaction_Status, User_id, Billing_Type, Billing_id):
        self.Cost = Cost
        self.Transaction_Date = Transaction_Date
        self.Transaction_Status =Transaction_Status
        self.User_id = User_id
        self.Billing_Type = Billing_Type
        self.Billing_id = Billing_id