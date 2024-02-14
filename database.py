# database.py

import mysql.connector

def connect_to_database():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="toor",
        password="N13#Br,9Kk",
        database="imagewebapp_db"
    )
