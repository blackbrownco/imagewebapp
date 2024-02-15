# app.py

import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, FileField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from user2 import register_user, login_user
from image import allowed_file, upload_image, retrieve_images, delete_image
from database import db_username, db_password
from models import LoginAttempt
from datetime import datetime, timedelta
from flask_wtf.csrf import validate_csrf
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_username}:{db_password}@localhost/imagewebapp_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)
UPLOAD_FOLDER = 'uploads/'


# Global variables for tracking attempts and cooldown
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_TIME = 120  # Account lock duration in seconds

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    image = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])

# Define record_login_attempt function to record login attempts in the database
def record_login_attempt(username):
    """Record login attempt in the database."""
    try:
        login_attempt = LoginAttempt(username=username, timestamp=datetime.now())
        db.session.add(login_attempt)
        db.session.commit()
    except Exception as e:
        print("Failed to record login attempt:", e)
        db.session.rollback()

@app.route('/')
def index():
    import os  # Add import for path handling
    images = [os.path.join("gambar", f"gambar{i}.jpg") for i in range(1, 5)]  
    return render_template("index.html", images=images)

@app.route('/usergallery', methods=['GET', 'POST'])
def usergallery():
    if 'username' in session:
        user_id = session['user_id']
        user_images = retrieve_images(user_id)
        form = UploadForm()

        if request.method == 'POST' and form.is_submitted():
            if form.validate():  
                if form.image.data:
                    filename = secure_filename(form.image.data.filename)
                    if upload_image(user_id, form.image.data):
                        return redirect(url_for('usergallery'))
                    else:
                        return "Upload failed. Please try again."
            return "Form validation failed. Please try again."

        return render_template('gallery.html', user_images=user_images, form=form)

    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    import os 
    images = [os.path.join("gambar", f"gambar{i}.jpg") for i in range(1, 5)]
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        if register_user(form.username.data, form.email.data, form.password.data):
            flash('Registration successful. You can now log in.', 'success')  # Display success message
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username or email already exists.', 'danger')  # Display error message
    return render_template('register.html', form=form, images=images)


from flask import redirect, url_for, flash

@app.route('/login', methods=['GET', 'POST'])
def login():
    import os
    images = [os.path.join("gambar", f"gambar{i}.jpg") for i in range(1, 5)]
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate():
            user_id = login_user(form.username.data, form.password.data)
            if user_id:
                session['username'] = form.username.data
                session['user_id'] = user_id
                flash('Login successful!', 'success')
                return redirect(url_for('usergallery'))
            else:
                flash('Invalid username or password. Please try again.', 'error')
            
    return render_template('login.html', form=form, images=images)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('user_id')
    return redirect(url_for('login'))

@app.route('/uploads/<user_id>/<path:filename>', methods=['GET'])
def uploaded_file(user_id, filename):
    user_folder = os.path.join(UPLOAD_FOLDER, user_id)
    return send_from_directory(user_folder, filename)


# @app.route('/uploads/:<path:filename>', methods=['POST'])
# def upload(filename):
#     form = UploadForm()
#     if form.validate_on_submit():
#         if 'username' in session:
#             user_id = session['user_id']
#             image_file = form.image.data
#             if image_file and allowed_file(image_file.filename):
#                 if upload_image(user_id, image_file):
#                     return redirect(url_for('index'))
#         return "Upload failed. Please try again."
#     return redirect(url_for('login'))

@app.route('/delete/<filename>')
def delete(filename):
    if 'username' in session:
        user_id = session['user_id']
        if delete_image(user_id, filename):
            return redirect(url_for('index'))
        return "Deletion failed. Please try again."
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
