"""
Class file for user data type
"""
from dataclasses import dataclass
from user import Professional as P, Client as C, Address as A, Billing as B, User_Security_Question as Q
from util.database import Database as db, DatabaseLookups as dl
import json


@dataclass
class User:
    user_id: int = None
    first_name: str = None
    last_name: str = None
    email_address: str = None  # doubles as username
    mobile: str = None
    password: str = None  # will be hashed
    address: A.Address = None
    client: C.Client = None  # possibly null
    professional: P.Professional = None  # possibly null
    cc_out: B.Billing = None
    cc_in: B.Billing = None
    security_questions: [Q.User_Security_Question] = None

    # SQL query to create user in User table
    def create_user(self):
        try:
            database = db.Database.database_handler(dl.DatabaseLookups.User.value)  # create database to connect to
            database.database_connect()  # connect to database
            query = "SELECT user_id FROM project.user WHERE email_address=%s"
            query_data = (self.email_address)
            validationcheck = database.database_query(query, query_data)
            if isinstance(validationcheck, int):
                return "User Already Exists"
        except Exception as e:
            print("Database Connection Error")
        query = ("INSERT INTO project.user "
                 "(firstname, lastname, email_address, mobile, password) "
                 "VALUES (%s, %s, %s, %s, %s)")
        query_data = (self.firstname, self.lastname, self.email_address, self.mobile, self.password)
        database.database_query(query, query_data)
        query = "SELECT user_id FROM project.user WHERE email_address=%s"
        query_data = self.email_address
        tuser_id = database.database_query(query, query_data)
        if not isinstance(tuser_id, int) or tuser_id < 0:
            return "User Creation Failed"
        self.user_id = tuser_id
        database.database_disconnect()

    def update_user(self):
        try:
            database = db.Database.database_handler(dl.DatabaseLookups.User.value)  # create database to connect to
            database.database_connect()  # connect to database
            query = "SELECT user_id FROM project.user WHERE user_id=%d"
            query_data = self.user_id
            validation_check = database.database_query(query, query_data)
            if not isinstance(validation_check, int) or validation_check < 0:
                return "invalid id"
        except Exception as e:
            print("Database Connection Error")
        query = ("UPDATE project.user "
                 "firstname = %s, lastname = %s, email_address = %s, mobile = %s, password = %s "
                 "WHERE user_id = %d")
        query_data = (self.firstname, self.lastname, self.email_address, self.mobile, self.password, self.user_id)
        database.database_query(query, query_data)
        query = "SELECT user_id FROM project.user WHERE email_address=%s"
        query_data = self.email_address
        tuser_id = database.database_query(query, query_data)
        if not isinstance(tuser_id, int) or tuser_id < 0:
            return "User update Failed"
        self.user_id = tuser_id
        database.database_disconnect()

    # return user object (possibly in json form)
    def get_user(self):
        my_json = """
                {
                  "userID": -1,
                  "firstname": "Snoop",
                  "lastname": "Dogg",
                  "email": "myemail@email.com",
                  "password": "myPassword123!!",
                  "mobile": "3344003626",
                  "address": {
                    "streetname": "Sesame Street",
                    "streetnumber": 7,
                    "suburb": "Liverpool",
                    "postcode": "2170"
                  },
                  "client": {
                    "membershiptype": "subscription"
                  },
                  "professional": {
                    "services": ["Not", "Implemented", "inDBYet"],
                    "CCin": {
                    "CCname": "John",
                    "CCnumber": "1234 5678 9123 456",
                    "expirydate": "11/2024",
                    "cvv": "123",
                    "billing_type": "In"
                    }
                  },
                  "CCout": {
                    "CCname": "Johny",
                    "CCnumber": "1224 5678 9123 456",
                    "expirydate": "11/2024",
                    "cvv": "133",
                    "billing_type": "Out"
                  },
                  "securityquestions": [
                    {
                      "security_question": "Question 1",
                      "answer": "Question 1 Answer"
                    },
                    {
                      "security_question": "Question 2",
                      "answer": "Question 2 Answer"
                    },
                    {
                      "security_question": "Question 3",
                      "answer": "Question 3 Answer"
                    }
                  ]
                }
                """
        user_dict = json.loads(my_json)
        user_dict['userID'] = self.user_id
        user_dict['firstname'] = self.firstname
        user_dict['lastname'] = self.lastname
        user_dict['email'] = self.email
        user_dict['password'] = self.password
        user_dict['mobile'] = self.mobile
        user_dict['address']['streetname'] = self.address.street_name
        user_dict['address']['streetnumber'] = self.address.street_number
        user_dict['address']['suburb'] = self.address.suburb
        user_dict['address']['postcode'] = self.address.postcode
        if not self.client is None:
            user_dict['client']['membershiptype'] = self.client.get_membershiptype()
        else:
            user_dict['client'] = {}
        if not self.professional is None:
            user_dict['professional']['CCin']['CCname'] = self.cc_in.name
            user_dict['professional']['CCin']['CCnumber'] = self.cc_in.card_number
            user_dict['professional']['CCin'][
                'expirydate'] = "" + self.cc_in.expiry_date.month + "/" + self.cc_in.expiry_date.year
            user_dict['professional']['CCin']['ccv'] = self.cc_in.cvv
            user_dict['professional']['CCin']['billing_type'] = "In"
        else:
            user_dict['professional'] = {}
        user_dict['CCout']['CCname'] = self.cc_out.name
        user_dict['CCout']['CCnumber'] = self.cc_out.card_number
        user_dict['CCout'][
            'expirydate'] = "" + self.cc_out.expiry_date.month + "/" + self.cc_out.expiry_date.year
        user_dict['CCout']['ccv'] = self.cc_out.cvv
        user_dict['CCout']['billing_type'] = "Out"
        for question_index in range(3):
            user_dict['securityquestions'][question_index]['security_question'] = self.security_questions[
                question_index].get_question()
            user_dict['securityquestions'][question_index]['answer'] = self.security_questions[
                question_index].answer
        return user_dict

    def create_json(self):
        my_json = """
        {
          "userID": -1,
          "firstname": "Snoop",
          "lastname": "Dogg",
          "email": "myemail@email.com",
          "password": "myPassword123!!",
          "mobile": "3344003626",
          "address": {
            "streetname": "Sesame Street",
            "streetnumber": 7,
            "suburb": "Liverpool",
            "postcode": "2170"
          },
          "client": {
            "membershiptype": "subscription"
          },
          "professional": {
            "services": ["Not", "Implemented", "inDBYet"],
            "CCin": {
            "CCname": "John",
            "CCnumber": "1234 5678 9123 456",
            "expirydate": "11/2024",
            "cvv": "123",
            "billing_type": "In"
            }
          },
          "CCout": {
            "CCname": "Johny",
            "CCnumber": "1224 5678 9123 456",
            "expirydate": "11/2024",
            "cvv": "133",
            "billing_type": "Out"
          },
          "securityquestions": [
            {
              "security_question": "Question 1",
              "answer": "Question 1 Answer"
            },
            {
              "security_question": "Question 2",
              "answer": "Question 2 Answer"
            },
            {
              "security_question": "Question 3",
              "answer": "Question 3 Answer"
            }
          ]
        }
        """
        user_dict = json.loads(my_json)
        user_dict['userID'] = self.user_id
        user_dict['firstname'] = self.firstname
        user_dict['lastname'] = self.lastname
        user_dict['email'] = self.email
        user_dict['password'] = self.password
        user_dict['mobile'] = self.mobile
        user_dict['address']['streetname'] = self.address.street_name
        user_dict['address']['streetnumber'] = self.address.street_number
        user_dict['address']['suburb'] = self.address.suburb
        user_dict['address']['postcode'] = self.address.postcode
        if not self.client is None:
            user_dict['client']['membershiptype'] = self.client.get_membershiptype()
        else:
            user_dict['client'] = {}
        if not self.professional is None:
            user_dict['professional']['CCin']['CCname'] = self.cc_in.name
            user_dict['professional']['CCin']['CCnumber'] = self.cc_in.card_number
            user_dict['professional']['CCin'][
                'expirydate'] = "" + self.cc_in.expiry_date.month + "/" + self.cc_in.expiry_date.year
            user_dict['professional']['CCin']['ccv'] = self.cc_in.cvv
            user_dict['professional']['CCin']['billing_type'] = "In"
        else:
            user_dict['professional'] = {}
        user_dict['CCout']['CCname'] = self.cc_out.name
        user_dict['CCout']['CCnumber'] = self.cc_out.card_number
        user_dict['CCout'][
            'expirydate'] = "" + self.cc_out.expiry_date.month + "/" + self.cc_out.expiry_date.year
        user_dict['CCout']['ccv'] = self.cc_out.cvv
        user_dict['CCout']['billing_type'] = "Out"
        for question_index in range(3):
            user_dict['securityquestions'][question_index]['security_question'] = self.security_questions[
                question_index].get_question()
            user_dict['securityquestions'][question_index]['answer'] = self.security_questions[
                question_index].answer

