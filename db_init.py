import sqlite3 as sq3

connection = sq3.connect('passwords.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE passwords (
                web_name text, 
                username text,
                password varchar(250))
""")

connection.commit()
connection.close()
