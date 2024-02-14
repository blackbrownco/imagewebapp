# app.py

from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField
from wtforms.validators import DataRequired
from user2 import register_user, login_user
from image import allowed_file, upload_image, retrieve_images, delete_image

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    image = FileField('Image', validators=[DataRequired()])
    submit = SubmitField('Upload')

#app.static_folder = 'static'

@app.route('/')
def index():
    import os  # Add import for path handling
    images = [os.path.join("gambar", f"gambar{i}.jpg") for i in range(1, 5)]  # Dynamically build image paths
    return render_template("index.html", images=images)

@app.route('/userpage')
def userpage():
    if 'username' in session:
        user_images = retrieve_images(session['user_id'])
        return render_template('gallery.html', user_images=user_images)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    import os  # Add import for path handling
    images = [os.path.join("gambar", f"gambar{i}.jpg") for i in range(1, 5)]
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        if register_user(form.username.data, form.email.data, form.password.data):
            return redirect(url_for('login'))
        else:
            return "Registration failed. Please try again."
    return render_template('register.html', form=form, images=images)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = login_user(form.username.data, form.password.data)
        if user:
            session['username'] = form.username.data
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            return "Login failed. Please try again."
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        if 'username' in session:
            user_id = session['user_id']
            image_file = form.image.data
            if image_file and allowed_file(image_file.filename):
                if upload_image(user_id, image_file):
                    return redirect(url_for('index'))
        return "Upload failed. Please try again."
    return redirect(url_for('login'))

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
