from db_connect import *
from sql_gen import *
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_KEY")
model = connect_gemini(api_key)

dbms = input("What Database Manaement System would you like to connect to?\n" \
             "[1] MySQL\n" \
             "[2] PostgreSQL\n\n")

if dbms == "1":
    db = input("What database do you want to connect to? ")
    host = os.getenv("MYSQL_HOST")
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    port = os.getenv("MYSQL_PORT")
    conn = connect_mysql(host, db, user, password, port)
    context = get_context_mysql(conn)

elif dbms == "2":
    db = input("What database do you want to connect to? ")
    host = os.getenv("PGSQL_HOST")
    user = os.getenv("PGSQL_USER")
    password = os.getenv("PGSQL_PASSWORD")
    port = os.getenv("PGSQL_PORT")
    conn = connect_pgsql(host, db, user, password, port)
    context = get_context_pgsql(conn)

else:
    raise ValueError("Invalid DBMS selection.")

while True:
    search = input("Your search: ")
    query = generate_query(context, search, model)
    if query:
        print(query)
        result, desc = send_query(conn, query)
    else:
        break

    if desc and result:
        print(desc)
        print(result)