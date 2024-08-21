import re, datetime, os
import mysql.connector

def clean_list(query):
    query = [x.replace('\r', '').replace('\n', '').strip() for x in query]

    query = [x for x in query if x != '']

    query = re.sub(' +', ' ', query[0]).split("/")

    query = [i.strip() for i in query if i != ""]

    return query

def get_today():
    return datetime.date.today()

def define_connection():
    """returns live connection to database"""

    user = os.environ['MY_USER']
    password = os.environ['MY_PWD'] 

    #for mysql
    return mysql.connector.connect(
        user=user,password=password,host='mysql',port='3306',database='db'
    )