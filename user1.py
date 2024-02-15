import bcrypt
import uuid
from datetime import datetime, timedelta
from flask import Flask
from flask_simple_captcha import CAPTCHA
from database import connect_to_database

app = Flask(__name__)  # Create a Flask app instance for Captcha
app.secret_key = 'your_secret_key'  # Replace with your Flask secret key
captcha = CAPTCHA(config={'SECRET_KEY': 'your_captcha_secret_key'})  # Replace with your Captcha secret key
app = captcha.init_app(app)

def register_user(username, email, password):
    """Register a new user."""
    user_id = str(uuid.uuid4())  # Generate a UUID as a string
    password_hash, salt = generate_password_hash(password)

    if not password_hash or not salt:
        return False

    db = connect_to_database()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (uuid, username, email, password_hash, salt) VALUES (%s, %s, %s, %s, %s)",
            (user_id, username, email, password_hash, salt)
        )
        db.commit()
        return True
    except Exception as e:
        print("Error during registration:", e)
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()

def login_user(username, password):
    """Login user and authenticate, with Captcha challenge and account locking."""
    db = connect_to_database()
    cursor = db.cursor()

    # Check if user exists and retrieve login attempts
    cursor.execute("""
        SELECT uuid, password_hash, salt, login_attempts, locked_until
        FROM users
        WHERE username = %s
    """, (username,))
    user_data = cursor.fetchone()

    # Handle non-existent user or errors
    if not user_data:
        return None

    user_id, stored_password_hash, salt, login_attempts, locked_until = user_data

    # Check account locking
    if locked_until and locked_until > datetime.utcnow():
        return None  # Account is locked

    # Check login attempts and Captcha
    if login_attempts >= 3:
        # Display Captcha challenge and validate
        if not request.form.get('captcha'):
            return render_template('login.html', captcha=captcha.generate())  # Assuming a login.html template
        elif not captcha.validate(request.form.get('captcha')):
            return render_template('login.html', error='Invalid Captcha', captcha=captcha.generate())

    # Verify password
    if verify_password(password, stored_password_hash, salt):
        # Successful login
        cursor.execute("UPDATE users SET login_attempts = 0 WHERE uuid = %s", (user_id,))
        db.commit()
        return user_id
    else:
        # Incorrect password, increment attempts and potentially lock account
        cursor.execute("UPDATE users SET login_attempts = login_attempts + 1 WHERE uuid = %s", (user_id,))
        if login_attempts >= 5:
            locked_until = datetime.utcnow() + timedelta(seconds=180)
            cursor.execute("UPDATE users SET locked_until = %s WHERE uuid = %s", (locked_until, user_id))
        db.commit()
        return None

    # Close connections
    cursor.close()
    db.close()

def generate_password_hash(password):
    """Generate password hash using bcrypt."""
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8') if password_hash else None

def verify_password(password, stored_password_hash):
    """Verify password against stored password hash."""
    return bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8'))
