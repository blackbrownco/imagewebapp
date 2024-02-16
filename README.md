# Image Storage Web Application

This is a simple web application for storing and managing images in a user's gallery.

## Features

- User registration and login system. (using uuid to prevent ID guessing that leads to IDOR vulnerability).
- Upload images to the user's gallery. (Image encyrption for the next version)
- View uploaded images in a gallery.
- Delete uploaded images from the gallery.

## Technologies Used

- Python
- Flask (Python web framework)
- SQLAlchemy (Python SQL toolkit and Object-Relational Mapping)
- MySQL (Relational Database Management System)
- HTML/CSS (Frontend)
- JavaScript (Frontend)

## Installation

1. Clone this repository to your local machine:
```bash
git clone <repository-url>
```
2.  Install the required dependencies using pip:
```bash
pip3 install -r requiremenets.txt
```
3. Set up a MySQL database:

   - Create a new MySQL database for the application.
   - Update the database connection details in `database.py` with your MySQL database credentials.

   ```python
   # database.py

   db_username = 'your_database_username'
   db_password = 'your_database_password'
   db_name = 'your_database_name'
   ```

   - Make 2 tables for users and images
     
     user table scheme:
   ```sql
    CREATE TABLE 'users' (
    uuid varchar(36) NOT NULL,
    username varchar(50) NOT NULL,
    email varchar(100) NOT NULL,
    password_hash varchar(100) NOT NULL,
    salt varchar(100) NOT NULL,
    created_at timestamp NULL DEFAULT current_timestamp(),
    PRIMARY KEY ('uuid')
    ```
    
    images table scheme:
    
    ```sql
    CREATE TABLE images (
    id int(11) NOT NULL AUTO_INCREMENT,
    user_id varchar(36) NOT NULL,
    username varchar(255) NOT NULL,
    filename varchar(255) NOT NULL,
    created_at timestamp NULL DEFAULT current_timestamp(),
    PRIMARY KEY ('id'),
    KEY 'user_id` ('user_id'),
    CONSTRAINT 'images_ibfk_1' FOREIGN KEY ('user_id') REFERENCES 'users' ('uuid')
    ```

4. Run the flask application:
   ```bash
   python3 app.py
   ```



