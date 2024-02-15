import bcrypt
import uuid
from database import connect_to_database
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def register_user(username, email, password):
    """Register a new user."""
    password_hash, salt = generate_password_hash(password)
    
    if not password_hash or not salt:
        return False
    
    db = connect_to_database()
    cursor = db.cursor()
    
    try:
        # Check if username or email already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s OR email = %s", (username, email))
        count = cursor.fetchone()[0]
        if count > 0:
            return False  # User with the same username or email already exists
        
        # Proceed with registration
        user_uuid = str(uuid.uuid4())  # Generate a UUID as a string
        cursor.execute("INSERT INTO users (uuid, username, email, password_hash, salt) VALUES (%s, %s, %s, %s, %s)",
                       (user_uuid, username, email, password_hash, salt))
        db.commit()
        return True  # Registration successful
    except Exception as e:
        print("Error:", e)
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()


def login_user(username, password):
    """Login user and authenticate."""
    print("Attempting to log in user:", username)
    try:
        db = connect_to_database()
        cursor = db.cursor()
        cursor.execute("SELECT uuid, password_hash, salt FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        print("Retrieved user data:", user_data)

        if user_data:
            uuid, stored_password_hash, salt = user_data
            password = password.strip()
            print("Input password1:", password)
            print("Stored password hash1:", stored_password_hash)
            print("Salt1:", salt)
            if verify_password(password, stored_password_hash, salt):
                print("Password verified. Login successful.")
                return uuid
        print("Login failed. Invalid username or password.")
        return None
    except Exception as e:
        print("An error occurred during login:", e)
        return None
    finally:
        cursor.close()
        db.close()


def generate_password_hash(password):
    """Generate password hash using bcrypt."""
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    print("Generated salt:", salt)
    print("Generated password hash:", password_hash)
    return password_hash.decode('utf-8'), salt.decode('utf-8')

# def verify_password(password, stored_password_hash, salt):
#     """Verify password against stored password hash."""
#     print("Input password:", password)
#     print("Stored password hash:", stored_password_hash)
#     print("Salt:", salt)
#     try:
#         # Ensure that the password length is within reasonable limits
#         if len(password) <= 72:  # Maximum password length supported by bcrypt
#             result = bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8') + salt.encode('utf-8'))
#             hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))
#             print("hashed retrieved password:", hashed_password.decode('utf-8'))
#             print("Result:", result)
#             return result
#         else:
#             print("Password length exceeds bcrypt limits.")
#             return False
#     except Exception as e:
#         print("An error occurred during password verification:", e)
#         return False
    
def verify_password(password, stored_password_hash, salt):
    """Verify password against stored password hash."""
    print("Input password:", password)
    print("Stored password hash:", stored_password_hash)
    print("Salt:", salt)
    try:
        # Concatenate the stored password hash and salt before decoding
        stored_password = stored_password_hash.encode('utf-8') + salt.encode('utf-8')
        # Hash the provided password with the stored salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))
        print("Hashed password:", hashed_password)
        # Compare the hashed password with the stored password hash
        result = hashed_password == stored_password_hash.encode('utf-8')
        print("Result:", result)
        return result
    except Exception as e:
        print("An error occurred during password verification:", e)
        return False

