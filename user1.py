import bcrypt
import uuid
from database import connect_to_database

def register_user(username, password):
    """Register a new user."""
    user_id = str(uuid.uuid4())  # Generate a UUID for user ID
    password_hash = generate_password_hash(password)
    if not password_hash:
        return False
    
    db = connect_to_database()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (user_id, username, password_hash) VALUES (%s, %s, %s)",
                       (user_id, username, password_hash))
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
    cursor.execute("SELECT user_id, password_hash FROM users WHERE username = %s", (username,))
    user_data = cursor.fetchone()
    cursor.close()
    db.close()
    
    if user_data:
        user_id, stored_password_hash = user_data
        if verify_password(password, stored_password_hash):
            return user_id
    return None

def generate_password_hash(password):
    """Generate password hash using bcrypt."""
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8') if password_hash else None

def verify_password(password, stored_password_hash):
    """Verify password against stored password hash."""
    return bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8'))
