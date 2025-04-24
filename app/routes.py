
from app import myapp_obj
from flask import render_template, redirect, request, flash
from app.forms import LoginForm, RegisterForm
from app.models import User
from app import db
from flask_login import current_user, login_required, login_user, logout_user

# Login route (landing page), renders home page and displays all recipes
#@myapp_obj.route("/")
#def login():
#    return render_template("login.html", title = "Log In", pageClass = "login")  # Render home.html

# Register route, renders home page and displays all recipes
@myapp_obj.route("/register")
def register():
    return render_template("register.html", title = "Register", pageClass = "register")  # Render home.html


# Home route, renders home page and displays all recipes
@myapp_obj.route("/home")
def home():
    return render_template("home.html", title = "Home", pageClass = "home")  # Render home.html

# All recipes tags route, renders home page and displays the page where you can select tags to see recipes.
@myapp_obj.route("/home/allrecipestagspage")
def allrecipestags():
    return render_template("allrecipestagspage.html", title = "All Recipes Tags", pageClass = "allrecipestagspage")  # Render home.html

# My recipes route, renders myrecipes page and displays all recipes
@myapp_obj.route("/home/myrecipes")
def myrecipes():
    return render_template("myrecipes.html", title = "My Recipes", pageClass = "myrecipes")  # Render home.html

# Following route, renders myrecipes page and displays all recipes
@myapp_obj.route("/home/following")
def following():
    return render_template("following.html", title = "Following", pageClass = "following")  # Render home.html

# My profile route, renders myrecipes page and displays all recipes
@myapp_obj.route("/home/myprofile")
def myprofile():
    return render_template("myprofile.html", title = "My Profile", pageClass = "myprofile")  # Render home.html

# Route when you click on your recipe, renders myrecipes page and displays all recipes
@myapp_obj.route("/home/myrecipes/mysinglerecipeview")
def mysinglerecipeview():
    return render_template("mysinglerecipeview.html", title = "My Recipe", pageClass = "mysinglerecipeview")  # Render home.html

# Route when you click "add recipe" on "my recipes" page, renders myrecipes page and displays all recipes
@myapp_obj.route("/home/myrecipes/mysinglerecipeadd")
def mysinglerecipeadd():
    return render_template("mysinglerecipeadd.html", title = "Add A Recipe", pageClass = "mysinglerecipeadd")  # Render home.html

# Route for logging out the user
@myapp_obj.route('/logout')
def logout():
    logout_user()  # Log the user out
    return redirect('/')  # Redirect to the homepage


# --------------------------------------------------------------------- #
# |                                                                    |#
# |                         User Related Routes                        |#
# |                                                                    |#
# --------------------------------------------------------------------- #
# Route for logging in the user
@myapp_obj.route('/login', methods=['GET', 'POST'])
@myapp_obj.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # If the user is already logged in, redirect to the homepage
    if current_user.is_authenticated:
        return redirect('/homepage')

    # Check if the form is submitted and passes validation (e.g., required fields are filled)
    if form.validate_on_submit():
        # Look for a user in the database with the provided email
        user = User.query.filter_by(email=form.email.data).first()

        # If a user exists and the password is correct, log the user in
        if user and user.check_password(form.password.data):
            login_user(user)  # Log the user in using Flask-Login
            return redirect('/homepage')  # Redirect to homepage after successful login
        else:
            # Flash an error message if email or password is incorrect
            flash("Invalid email or password", "danger")

    # If it's a POST request but the form didn't validate (e.g., missing fields), show a generic warning
    elif request.method == 'POST':
        flash("Please fill out all fields correctly.", "danger")

    # Render the login form template with the form object passed in
    return render_template("test_login.html", form=form)

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
    


