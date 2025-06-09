import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    database="employees",
    user="root",
    password="12345678",
    port=3306
)

cursor = conn.cursor()
cursor.execute("show tables;")
tables = cursor.fetchall()

for t in tables:
    cursor.execute(f"describe {t[0]};")
    desc = cursor.fetchall()
    print(t[0])
    for a in desc:
        print(f"Attribute: {a[0]}\n" \
                f"Type: {a[1]}\n" \
                f"Null: {a[2]}\n" \
                f"Key: {a[3]}\n" \
                f"Default: {a[4]}\n"
                f"Extra: {a[5]}\n")
    print("\n\n")