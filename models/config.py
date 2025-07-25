import sqlite3
from database import create_database

def initialize_table():
    create_database()
    conn = sqlite3.connect("Parking.db")
    curr = conn.cursor()

    admin_username = "admin"
    admin_password = "admin"


    curr.execute('''INSERT OR IGNORE INTO ADMIN(username,password) VALUES(?,?);''',(admin_username,admin_password)) #insert admin cred into table and ignore if already exists

    conn.execute()
    conn.close()

    print("Admin credentials added into tabke /n")