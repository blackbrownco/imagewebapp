# database.py

import mysql.connector

def connect_to_database():
    """Connect to the MySQL database."""
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="toor",
            password="N13#Br,9Kk",
            database="imagewebapp_db"
    )
        return db
    except mysql.connector.Error as e:
        print("Error connecting to database:", e)
        return None

db_username = "toor"
db_password = "N13#Br,9Kk"