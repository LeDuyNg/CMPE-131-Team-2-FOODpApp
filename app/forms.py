from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

# Login form for user authentication
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(message="Please enter a valid email address.")])  # Email field, requires data
    password = PasswordField('Password', validators=[Length(min=4, max=35)])  # Password field with a length constraint
    submit = SubmitField("Sign in")  # Submit button with the label "Sign in"

# Form for creating a new account
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Username field, requires data
    password = PasswordField('Password', validators=[Length(min=4, max=35)])  # Password field with length constraint
    email = EmailField('Email', validators=[DataRequired(), Email(message="Please enter a valid email address.")])  # Email field, requires data
    submit = SubmitField("Register Account")  # Submit button with the label "Create Account"ta