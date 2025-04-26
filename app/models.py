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

class Recipe(db.Model):
    # Define columns for the Recipe table
    id = db.Column(db.Integer, primary_key=True)  # Primary key for recipe ID
    title = db.Column(db.String(80))  # Column for recipe title with a max length of 80 characters
    description = db.Column(db.Text, nullable=False)  # Column for recipe description (non-nullable)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    created = db.Column(db.DateTime, default=datetime.now())  # Timestamp for when the recipe is created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to associate with a User
    created = db.Column(db.DateTime, default=datetime.now())
    num_of_rating = db.Column(db.Integer, default=0)
    total_rating = db.Column(db.Integer, default=0)
    tags = db.Column(db.JSON, default=[])

    def rate_recipe(self, rating):
        self.total_rating += rating
        self.num_of_rating += 1
        db.session.commit()

    def set_title(self, new_title):
        self.title = new_title
        db.session.commit()

    def get_title(self):
        return self.title

    def set_description(self, new_description):
        self.description = new_description
        db.session.commit()

    def get_description(self):
        return self.description

    def set_instructions(self, new_instructions):
        self.instructions = new_instructions
        db.session.commit()

    def get_instructions(self):
        return self.instructions

    def set_ingredients(self, new_ingredients):
        self.ingredients = new_ingredients
        db.session.commit()

    def get_ingredients(self):
        return self.ingredients
    
    # Function to format the ingredients as a list from a comma-separated string
    def format_ingredients(self, unformatted_list):
        """Converts a comma-separated string into a list, stripping any extra spaces"""
        if not unformatted_list:  # Check if the list is empty
            return []
        return [element.strip() for element in unformatted_list.split('\n')]  # Split by newline and strip extra spaces

    # Function to format the instructions as a list from a dot-separated string
    def format_instructions(self, unformatted_list):
        """Converts a dot-separated string into a list, stripping any extra spaces"""
        if not unformatted_list:  # Check if the list is empty
            return []
        return [element.strip() for element in unformatted_list.split('.')]  # Split by dot and strip extra spaces

    # def set_tags(self, new_tags):
    #     self.tags = json.dumps(new_tags)
    #     db.session.commit()
    #
    # def get_tags(self):
    #     try:
    #         return json.loads(self.tags)
    #     except (TypeError, json.JSONDecodeError):
    #         return []