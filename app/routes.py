from app import myapp_obj
from flask import render_template, redirect, request, flash
from app.forms import LoginForm, RegisterForm
from app.models import User
from app import db
from flask_login import current_user, login_required, login_user, logout_user

# --------------------------------------------------------------------- #
# |                                                                    |#
# |                         User Related Routes                        |#
# |                                                                    |#
# --------------------------------------------------------------------- #
# Route for logging in the user
@myapp_obj.route('/login', methods=['GET', 'POST'])
@myapp_obj.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create form for user to log in
    if current_user.is_authenticated:  # If the user is already logged in
        return redirect('/homepage')  # Redirect to the home page

    if request.method == 'POST':  # If the form is submitted
        user = User.query.filter_by(email=form.email.data).first()  # Query for the user by username
        if user is not None and user.check_password(password=form.password.data):  # Check if the password is correct
            login_user(user)  # Log the user in
            return redirect("/homepage")  # Redirect to the home page
        else:
            flash("Invalid email or password", "danger")  # Show an error message if login fails
    return render_template("test_login.html", form=form)  # Render login.html and pass the form

# Route for creating a new user account
@myapp_obj.route("/register_account", methods=['GET', 'POST'])
def register_account():
    form = RegisterForm()  # Create form for user to create an account
    if form.validate_on_submit():  # Validate the form when the user submits it
        # Create a new user and hash their password
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)  # Add the user to the session
        db.session.commit()  # Commit the changes to the database
        return redirect("/")  # Redirect to the homepage after account creation
    else:
        return render_template("test_register_account.html", title="Create Account", form=form)
    
# Route for logging out the user
@myapp_obj.route('/logout')
def logout():
    logout_user()  # Log the user out
    return redirect('/')  # Redirect to the homepage

# Route for the home page
@myapp_obj.route('/homepage')
@login_required  # Require the user to be logged in to access this page
def homepage():
    return render_template("test_homepage.html")