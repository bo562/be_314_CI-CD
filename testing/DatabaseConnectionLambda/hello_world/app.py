import json
import mysql.connector

# import requests

def lambda_handler(event, context):
    cnx = mysql.connector.connect(user='lambda',password='KFYD8395',host='csit314-gp.crjrzvrrbory.us-east-1.rds.amazonaws.com', database='Lambda_Test')
    
    with cnx.cursor() as cursor:
        query = ("SELECT idTest,Testcol "
        "FROM Test")
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)

    return {}
