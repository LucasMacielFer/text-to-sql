from db_connect import *
from sql_gen import *
from dataframe import *
import os
from dotenv import load_dotenv

def start_services():
    load_dotenv()
    api_key = os.getenv("GEMINI_KEY")
    model = connect_gemini(api_key)

    dbms_selected = False

    while not dbms_selected:
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
            if conn:
                dbms_selected = True
                context = get_context_mysql(conn)


        elif dbms == "2":
            db = input("What database do you want to connect to? ")
            host = os.getenv("PGSQL_HOST")
            user = os.getenv("PGSQL_USER")
            password = os.getenv("PGSQL_PASSWORD")
            port = os.getenv("PGSQL_PORT")
            conn = connect_pgsql(host, db, user, password, port)
            if conn:
                dbms_selected = True
                context = get_context_pgsql(conn)


        else:
            print("Invalid DBMS selection.\n")
    
    chat = start_chat(model, context)
    return chat, conn

def search_db(chat, conn):
    df = None
    desc = None
    result = None
    search = input("Search in database: ")
    query = generate_query(search, chat)

    if query:
        result, desc = send_query(conn, query)

    if desc and result:
        df = create_df(desc, result)

    return df

def manage_saving(df):
    options = ["xml", "csv", "xlsx", "json", None]
    print("\n"\
                "How would you like to store your data?\n"\
                "[1] Save data as XML file\n" \
                "[2] Save data as CSV file\n" \
                "[3] Save data as EXCEL table\n" \
                "[4] Save data as JSON file\n")

    op = input("Select: ")

    if op.lower() not in ["1", "2", "3", "4"]:
        op = 4
    
    selection = options[int(op)-1]
    if selection:
        export(df, selection)

def main():
    chat, conn = start_services()
    exit = False
    while not exit:
        df = search_db(chat, conn)
        if df:
            print_data(df)
            save = input("Would you like to store your data? [Y/N] ")

            if save.lower() in ["y", "yes"]:
                manage_saving(df)

        leave = input("Would you like to make another search? [Y/N] ")
        if leave.lower() in ["no", "n"]:
            exit = True

if __name__=="__main__":
    main()