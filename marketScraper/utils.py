import re, datetime, sqlite3

def clean_list(query):
    query = [x.replace('\r', '').replace('\n', '').strip() for x in query]

    query = [x for x in query if x != '']

    query = re.sub(' +', ' ', query[0]).split("/")

    query = [i.strip() for i in query if i != ""]

    return query

def get_today():
    return datetime.date.today()

def define_connection():

    #for sqlite3
    return sqlite3.connect('../../example_database.sqlite')