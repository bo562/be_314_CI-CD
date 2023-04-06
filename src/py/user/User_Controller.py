"""
py that describes the controller for the user sub-package. Enabling User creation, manipulation and
authentication/authorisation
"""
from types import SimpleNamespace
from util.database import Database
from user import User as U, Address as A, Subscription as S, Client as C, Professional as P, Billing as B, \
    User_Question as Q
from datetime import datetime
from mysql.connector.errors import Error
import json

class User_Controller:
    def __init__(self, data: str):
        self.data = data

    def create_user(self, data: str) -> U.User:
        try:
            userdata = json.loads(data)
            userinstance = U.User(-1, userdata['firstname'], userdata['lastname'], userdata['email'],
                                  userdata['mobile'], userdata['password'])
            userinstance.create_user()
            setattr(userinstance, 'address', A.Address(-1, userdata['address']['streetnumber'],
                                                       userdata['address']['streetname'], userdata['address']['suburb'],
                                                       userdata['address']['postcode']))
            userinstance.address.create_address(userinstance.user_id)

            setattr(userinstance, 'cc_out', B.Billing(-1, userdata['CCout']['CCname'], userdata['CCout']['CCnumber'],
                                                      datetime.strptime(('01' + userdata['CCout']['expirydate'][0:2] +
                                                                         userdata['CCout']['expirydate'][3:7]),
                                                                        "%d%m%Y").date(),
                                                      userdata['CCout']['ccv'], userdata['CCout']['billing_type']))
            userinstance.cc_out.create_billing(userinstance.user_id)
            if userdata['client']:
                setattr(userinstance, 'client', C.Client(-1))
                userinstance.client.create_client(userinstance.user_id, userdata['client']['membershiptype'])
            if userdata['professional']:
                setattr(userinstance, 'professional', P.Professional(-1))
                userinstance.professional.create_professional(userinstance.user_id)
                setattr(userinstance, 'cc_in', B.Billing(-1, userdata['professional']['CCin']['CCname'],
                                                         userdata['professional']['CCin']['CCnumber'],
                                                         datetime.strptime(('01' + userdata['professional']['CCin'][
                                                                                       'expirydate'][0:2] +
                                                                            userdata['professional']['CCin'][
                                                                                'expirydate'][3:7]), "%d%m%Y").date(),
                                                         userdata['professional']['CCin']['ccv'],
                                                         userdata['professional']['CCin']['billing_type']))
                userinstance.cc_in.create_billing(userinstance.user_id)
                array_index = 0
                for temp_question in userdata['securityquestions']:
                    userinstance.security_questions.append(Q.User_Security_Question(-1), temp_question['answer'])
                    userinstance.security_questions[array_index].create_question(userinstance.user_id,
                                                                                 temp_question['security_question'])
                    array_index += 1
                userjson = userinstance.get_user()
                out_file = open("myfile.json", "w")
                json.dump(userjson, out_file, indent=6)
        except Error as err:
            raise err

    def update_user(self, data: str) -> U.User:
        try:
            userdata = json.loads(data)
            userinstance = U.User(userdata['user_id'], userdata['firstname'], userdata['lastname'], userdata['email'],
                                  userdata['mobile'], userdata['password'])
            userinstance.update_user()
            setattr(userinstance, 'address', A.Address(-1, userdata['address']['streetnumber'],
                                                       userdata['address']['streetname'], userdata['address']['suburb'],
                                                       userdata['address']['postcode']))
            userinstance.address.update_address(userinstance.user_id)

            setattr(userinstance, 'cc_out', B.Billing(-1, userdata['CCout']['CCname'], userdata['CCout']['CCnumber'],
                                                      datetime.strptime(('01' + userdata['CCout']['expirydate'][0:2] +
                                                                         userdata['CCout']['expirydate'][3:7]),
                                                                        "%d%m%Y").date(),
                                                      userdata['CCout']['ccv'], userdata['CCout']['billing_type']))
            userinstance.cc_out.update_billing(userinstance.user_id)
            if userdata['client']:
                setattr(userinstance, 'client', C.Client(-1))
                userinstance.client.update_client(userinstance.user_id, userdata['client']['membershiptype'])
            if userdata['professional']:
                setattr(userinstance, 'professional', P.Professional(-1))
                userinstance.professional.update_professional(userinstance.user_id)
                setattr(userinstance, 'cc_in', B.Billing(-1, userdata['professional']['CCin']['CCname'],
                                                         userdata['professional']['CCin']['CCnumber'],
                                                         datetime.strptime(('01' + userdata['professional']['CCin'][
                                                                                       'expirydate'][0:2] +
                                                                            userdata['professional']['CCin'][
                                                                                'expirydate'][3:7]), "%d%m%Y").date(),
                                                         userdata['professional']['CCin']['ccv'],
                                                         userdata['professional']['CCin']['billing_type']))
                userinstance.cc_in.update_billing(userinstance.user_id)
                array_index = 0
                for temp_question in userdata['securityquestions']:
                    userinstance.security_questions.append(Q.User_Security_Question(-1), temp_question['answer'])
                    userinstance.security_questions[array_index].update_question(userinstance.user_id,
                                                                                 temp_question['security_question'])
                    array_index += 1
                userjson = userinstance.get_user()
                out_file = open("myfile.json", "w")
                json.dump(userjson, out_file, indent=6)
        except Error as err:
            raise err



