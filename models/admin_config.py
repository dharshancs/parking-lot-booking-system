import sqlite3
import sys
import os

# Add parent directory (project root) to the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import create_database


def config_admin():
    create_database() #To make sure that database is created before adding admin credentials

    conn = sqlite3.connect('parking_db')
    curr = conn.cursor()

    admin_username = 'admin'
    admin_password = 'admin'

    curr.execute('''INSERT OR IGNORE INTO ADMIN 
                 (username,password) VALUES (?,?);''',(admin_username,admin_password)) #Avoids redundancy
    
    conn.commit()
    conn.close()

config_admin()
    