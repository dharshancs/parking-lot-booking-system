import sqlite3

def create_database():
    conn = sqlite3.connect("Parking.db")       #connects and creates db if not available
    conn.execute("PRAGMA foreign_keys = ON")  # Since our table has foreign keys it enables foreign keys
    curr = conn.cursor()                       #cursor to execute queries

    curr.execute('''
                CREATE TABLE IF NOT EXISTS USERS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                address TEXT,
                pincode INTEGER,
                password TEXT NOT NULL
                );
                ''')
    curr.execute('''
                CREATE TABLE IF NOT EXISTS ADMIN(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL               
                );
                ''')
    curr.execute('''
                CREATE  TABLE IF NOT EXISTS PARKING_LOT(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prime_location TEXT NOT NULL,
                price INTEGER DEFAULT '250',
                address TEXT NOT NULL,
                pincode INTEGER NOT NULL,
                max_no_of_spots INTEGER NOT NULL DEFAULT '10'
                );
                ''')
    curr.execute('''CREATE TABLE IF NOT EXISTS PARKING_SPOT(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lot_id INTEGER NOT NULL,
                slot_number TEXT NOT NULL,
                status TEXT DEFAULT 'A',
                FOREIGN KEY(lot_id) REFERENCES PARKING_LOT(id) ON DELETE CASCADE
                ); 
                ''') 
    curr.execute('''CREATE TABLE IF NOT EXISTS booking_details(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                slot_id INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES USERS(id),
                FOREIGN KEY(slot_id) REFERENCES PARKING_SPOT(id)
                );
                ''')
    
    conn.commit()
    conn.close()


    #print("Database created succesfully/n")   ----> COULD NOT SEE ANY OUTPUT IN TERMINAL