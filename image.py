# image.py

import os
from werkzeug.utils import secure_filename
from database import connect_to_database

UPLOAD_FOLDER = 'uploads/'

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def upload_image(user_id, image_file):
    """Upload image for the user."""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(filepath)

        db = connect_to_database()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO images (user_id, filename) VALUES (%s, %s)", (user_id, filename))
            db.commit()
            return True
        except Exception as e:
            print("Error:", e)
            db.rollback()
            return False
        finally:
            cursor.close()
            db.close()
    else:
        return False

def retrieve_images(user_id):
    """Retrieve images for the user."""
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT filename FROM images WHERE user_id = %s", (user_id,))
    images = cursor.fetchall()
    cursor.close()
    db.close()
    return images

def delete_image(user_id, filename):
    """Delete image for the user."""
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    db = connect_to_database()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM images WHERE user_id = %s AND filename = %s", (user_id, filename))
        db.commit()
        return True
    except Exception as e:
        print("Error:", e)
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()
