from app import db  # Import the database instance from the app module
from datetime import datetime  # Import datetime to handle timestamps
from werkzeug.security import generate_password_hash, check_password_hash  # Import for password hashing
from flask_login import UserMixin  # Import UserMixin to integrate Flask-Login

# Define the User model, inheriting from UserMixin for Flask-Login functionality
class User(UserMixin, db.Model):
    # Define columns for the User table
    id = db.Column(db.Integer, primary_key=True)  # Primary key for user ID
    username = db.Column(db.String(32))  # Column for username with a max length of 32 characters
    password_hash = db.Column(db.String())  # Column to store hashed password
    email = db.Column(db.String(32))  # Column for user email
    # Uncomment this line if you want to add a relationship to recipes created by the user
    #recipes = db.relationship('Recipe', backref='author', lazy='dynamic')  # Relationship to recipes created by the user

    # Function to generate a hash for the password before storing it
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Function to check if the password matches the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Function to represent the user object as a string
    def __repr__(self):
        return '<Username {}>'.format(self.username)