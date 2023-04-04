import json


my_json = """
{
  "userID": 1,
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
  "professional": null,
  "CCin": {
    "CCname": "John",
    "CCnumber": "1234 5678 9123 456",
    "CCsecurity": "123"
  },
  "CCout": {
    "CCname": "John",
    "CCnumber": "1234 5678 9123 456",
    "CCsecurity": "123"
  },
  "securityquestions": [
    "CAR",
    "CAR",
    "CAR"
  ]
}
"""
js = json.loads(my_json)

print(js['securityquestions'])