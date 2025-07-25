import sqlite3
from .database import create_database   #If i dont use .database python will look from working database and not relative

def initialize_table():
    create_database()
    conn = sqlite3.connect("Parking.db")
    curr = conn.cursor()

    admin_username = "admin"
    admin_password = "admin"


    curr.execute('''INSERT OR IGNORE INTO ADMIN(username,password) VALUES(?,?);''',(admin_username,admin_password)) #insert admin cred into table and ignore if already exists

    conn.commit()
    conn.close()

    #print("Admin credentials added into tabke /n")