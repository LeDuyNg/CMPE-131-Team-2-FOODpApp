from email.policy import default

from app import db  # Import the database instance from the app module
from datetime import datetime  # Import datetime to handle timestamps
from werkzeug.security import generate_password_hash, check_password_hash  # Import for password hashing
from flask_login import UserMixin  # Import UserMixin to integrate Flask-Login
from sqlalchemy.orm.attributes import flag_modified
from flask.json import jsonify
import json

favorite_recipes = db.Table(
    'favorite_recipes',
    db.Column('user_id',    db.Integer, db.ForeignKey('user.id'),    primary_key=True),
    db.Column('recipe_id',  db.Integer, db.ForeignKey('recipe.id'),  primary_key=True),
)

# Define the User model, inheriting from UserMixin for Flask-Login functionality
class User(UserMixin, db.Model):
    # Define columns for the User table
    id = db.Column(db.Integer, primary_key=True)  # Primary key for user ID
    username = db.Column(db.String(32))  # Column for username with a max length of 32 characters
    password_hash = db.Column(db.String())  # Column to store hashed password
    email = db.Column(db.String(32))  # Column for user email
    # Uncomment this line if you want to add a relationship to recipes created by the user
    #recipes = db.relationship('Recipe', backref='author', lazy='dynamic')  # Relationship to recipes created by the user
    favorite_recipes  = db.relationship(
        'Recipe',
        secondary = favorite_recipes,
        backref=db.backref('favorited_by', lazy='dynamic'),
        lazy='dynamic'
    )


    # Function to generate a hash for the password before storing it
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Function to check if the password matches the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Function to update email address
    def update_email(self, email):
        self.email = email

    # Function to update username
    def update_username(self, username):
        self.username = username

    def add_favorite(self, recipe):
        if not self.favorite_recipes.filter_by(id=recipe.id).first():
            self.favorite_recipes.append(recipe)
            db.session.commit()

    def remove_favorite(self, recipe):
        if self.favorite_recipes.filter_by(id=recipe.id).first():
            self.favorite_recipes.remove(recipe)
            db.session.commit()

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
    comment_ids = db.Column(db.String, default="")

    created = db.Column(db.DateTime, default=datetime.now())  # Timestamp for when the recipe is created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to associate with a User
    created = db.Column(db.DateTime, default=datetime.now())
    num_of_rating = db.Column(db.Integer, default=0)
    total_rating = db.Column(db.Integer, default=0)
    tags = db.Column(db.JSON, default={})

    def fix_tags(self):
        if self.tags == []:
            self.tags = {}
        flag_modified(self, "tags")
        db.session.commit()
        
        
    def set_tags(self, new_tags):
        if self.tags == []:
            self.tags = {}
        for tag in new_tags:
            self.tags[tag] = new_tags[tag]
        flag_modified(self, "tags")
        db.session.commit()
    
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

    def set_comment_ids(self, new_comment_ids):
        self.comment_ids = new_comment_ids
        db.session.commit()

    def add_comment_id(self, comment_id):
        self.set_comment_ids(self.comment_ids + " " + str(comment_id))

    def get_comment_ids(self):
        return self.comment_ids.split()
    
    # This function check the comment ids and remove duplicates while reserving the order
    def update_comment_ids(self):
        seen = set()
        unique = []
        for cid in self.get_comment_ids():
            if cid not in seen:
                seen.add(cid)
                unique.append(cid)

        # store back as space-separated string
        self.comment_ids = " ".join(unique)
        flag_modified(self, "comment_ids")
        db.session.commit()

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

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    comment = db.Column(db.String)
    # replies = db.Column(db.String) # stores a list of comment id's
