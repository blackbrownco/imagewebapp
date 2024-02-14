# user.py

import uuid
from database import connect_to_database

def register_user(username, password):
    """Register a new user."""
    user_id = str(uuid.uuid4())  # Generate a UUID for user ID
    db = connect_to_database()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (user_id, username, password) VALUES (%s, %s, %s)", (user_id, username, password))
        db.commit()
        return True
    except Exception as e:
        print("Error:", e)
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()

def login_user(username, password):
    """Login user and authenticate."""
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    
    if user:
        if user[2] == password:  # Assuming password is stored in the third column
            return user
    return None
