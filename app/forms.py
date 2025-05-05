from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, validators, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

# Login form for user authentication
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(message="Please enter a valid email address.")])  # Email field, requires data
    password = PasswordField('Password', validators=[Length(min=4, max=35)])  # Password field with a length constraint
    submit = SubmitField("LOG IN")  # Submit button with the label "Sign in"

# Form for creating a new account
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Username field, requires data
    password = PasswordField('Password', validators=[Length(min=4, max=35)])  # Password field with length constraint
    email = EmailField('Email', validators=[DataRequired(), Email(message="Please enter a valid email address.")])  # Email field, requires data
    submit = SubmitField("Register Account")  # Submit button with the label "Create Account"ta


class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Username field, requires data
    password = PasswordField('Password', validators=[Length(min=4, max=35)])  # Password field with length constraint
    email = EmailField('Email', validators=[DataRequired(), Email(message="Please enter a valid email address.")])  # Email field, requires data
    submit = SubmitField("Update Account")  # Submit button with the label "Create Account"ta

class RecipeForm(FlaskForm):
    title = StringField("Title", validators=[validators.Length(min=1, max=80)])
    title_for_search = StringField("Title", validators=[validators.Length(max=80)])
    description = TextAreaField("Description", validators=[validators.DataRequired()])
    ingredients = TextAreaField("Ingredients", validators=[validators.DataRequired()])
    instructions = TextAreaField("Instructions", validators=[validators.DataRequired()])
    temperature = RadioField("Temperature", choices = [("hot", "Hot"), ("cold", "Cold"), ("", "Other")], default = "")
    dish_type = RadioField("Dish Type", choices = [("soups", "Soups"), ("salads", "Salads"), ("dessert", "Desserts"), ("main", "Main"), ("", "Other")], default = "")
    dairy = RadioField("Dairy", choices = [("dairy", "Dairy"), ("non-dairy", "Non-dairy"), ("", "Other")], default = "")
    sweetness = RadioField("Sweetness", choices = [("sweet", "Sweet"), ("savory", "Savory"), ("", "Other")], default = "")
    meat = RadioField("Meat", choices = [("meat", "Meat"), ("non-meat", "Non-meat"), ("", "Other")], default = "")
    seafood = RadioField("Seafood", choices = [("seafood", "Seafood"), ("non-seafood", "Non-seafood"), ("", "Other")], default = "")
    
    # tags = SelectMultipleField(
    #     'Tags',
    #     choices=[
    #         ('vegan', 'Vegan'),
    #         ('vegetarian', 'Vegetarian'),
    #         ('gluten_free', 'Gluten-Free'),
    #         ('quick', 'Quick'),
    #         ('healthy', 'Healthy')
    #     ],
    #     option_widget=CheckboxInput(),
    #     widget=ListWidget(prefix_label=False)
    # )
    submit_recipe =  SubmitField("submit recipe")

class CommentForm(FlaskForm):
    comment = TextAreaField("Comment", validators=[validators.DataRequired()])
    submit_comment =  SubmitField("submit comment")
