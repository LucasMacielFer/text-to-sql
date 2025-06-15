import mysql.connector
import psycopg2

def connect_mysql(host, database, user, password, port):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port)
        print(f"Connected succesfully to database {database} on MySQL.")

    except Exception as e:
        print(f"Failed to connect to database {database} on MySQL.")
    return conn

def connect_pgsql(host, database, user, password, port):
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        print(f"Connected succesfully to database {database} on PostgreSQL.")

    except Exception as e:
        print(f"Failed to connect to database {database} on PostgreSQL.")
    return conn

def get_context_mysql(conn):
    cursor = conn.cursor()
    context = "We are using MySQL\n\n"
    cursor.execute("show tables;")
    tables = cursor.fetchall()
    for t in tables:
        cursor.execute(f"describe {t[0]};")
        desc = cursor.fetchall()
        context += f"Table {t[0]} has columns:\n"

        for a in desc:
            context += f"Attribute: {a[0]}\n"
            context += f"Type: {a[1]}\n"
            context += f"Null: {a[2]}\n"
            context += f"Key: {a[3]}\n"
            context += f"Default: {a[4]}\n"
            context += f"Extra: {a[5]}\n\n"
    
    cursor.close()
    return context

def get_context_pgsql(conn):
    cursor = conn.cursor()
    context = "We are using PostgreSQL. \n\n"
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
    tables = cursor.fetchall()

    for t in tables:
        cursor.execute("SELECT column_name, data_type, character_maximum_length, is_nullable, column_default " \
                        "FROM information_schema.columns " \
                        f"WHERE table_name = '{t[0]}';")        
        desc = cursor.fetchall()
        context += f"Table {t[0]} has columns:\n\n"

        for a in desc:
            context += f"Attribute: {a[0]}\n"
            context += f"Type: {a[1]}\n"
            context += f"Max length: {a[2]}\n"
            context += f"Is nullable: {a[3]}\n"
            context += f"Default value: {a[4]}\n\n"
    
    cursor.close()
    return context

def close_connection(conn):
    if conn:
        conn.close()
        print("Connection closed.")

def send_query(conn, query):
    cursor = conn.cursor()
    result = None
    desc = None

    if "drop" in query.lower() or "insert" in query.lower() or "delete" in query.lower() or "alter" in query.lower():
        print("You don't have access to drop, insert, delete or alter.")
        return None, None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        desc = [d[0] for d in cursor.description]
    except Exception as e:
        print("Invalid search on database.")
    cursor.close()
    return result, desc