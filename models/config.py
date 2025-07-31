import sqlite3
from .database import create_database   #If i dont use .database python will look from working database and not relative
from werkzeug.security import generate_password_hash

def initialize_table():
    create_database()
    conn = sqlite3.connect("Parking.db")
    curr = conn.cursor()

    admin_id = 0
    admin_username = "admin@admin.com"
    admin_password = generate_password_hash("admin")
    is_admin = True


    curr.execute('''INSERT OR REPLACE INTO USERS(id,email,password,is_admin) VALUES(?,?,?,?);''',(admin_id,admin_username,admin_password,is_admin)) #insert admin cred into table and ignore if already exists

    conn.commit()
    conn.close()

    #print("Admin credentials added into tabke /n")
    

    