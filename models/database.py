import sqlite3

def create_database():
    conn = sqlite3.connect("parking_db")
    curr = conn.cursor()
    curr.execute('''CREATE TABLE IF NOT EXISTS USERS
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    USERNAME TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    print("Done")

create_database()