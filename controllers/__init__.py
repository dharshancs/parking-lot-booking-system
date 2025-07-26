import sqlite3

def conn_database():  #to connect to database for login and registration
    conection = sqlite3.connect('Parking.db')
    conection.row_factory = sqlite3.Row      #to convert tuple form to dictionary form
    return conection