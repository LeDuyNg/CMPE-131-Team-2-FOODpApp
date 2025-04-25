
from app import myapp_obj
from flask import render_template, redirect, request, flash
from app.forms import LoginForm, RegisterForm
from app.models import User
from app import db
from flask_login import current_user, login_required, login_user, logout_user

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

# --------------------------------------------------------------------- #
# |                                                                    |#
# |                         User Related Routes                        |#
# |                                                                    |#
# --------------------------------------------------------------------- #
# Route for logging in the user
@myapp_obj.route('/login', methods=['GET', 'POST'])
@myapp_obj.route('/', methods=['GET', 'POST'])
def login():
    # Create an instance of the login form
    form = LoginForm()

    # If the user is already authenticated, redirect them to the homepage
    if current_user.is_authenticated:
        return redirect('/home')
    
    # Check if the form is submitted and passes validation
    if form.validate_on_submit():
        # Query the database for a user with the entered email
        user = User.query.filter_by(email=form.email.data).first()

        # If user exists and password is correct, log them in and redirect to homepage
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/home')
        else:
            # Invalid email or password
            flash("Invalid email or password", "danger")
    
    # If request method is POST but validation failed (e.g., empty or invalid fields)
    elif request.method == 'POST':
        flash("Please fill out all fields correctly.", "danger")

    # Render the login page with the form
    return render_template("login.html", title="Login", form=form, pageClass="login")



# Route for creating a new user account
@myapp_obj.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # Create form for user to create an account
    if form.validate_on_submit():  # Validate the form when the user submits it
        # Create a new user and hash their password
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)  # Add the user to the session
        db.session.commit()  # Commit the changes to the database
        return redirect("/")  # Redirect to the homepage after account creation
    else:
        return render_template("register.html", title = "Register", pageClass = "register", form=form)
    
# Route for logging out the user
@myapp_obj.route('/logout')
def logout():
    logout_user()  # Log the user out
    return redirect('/')  # Redirect to the homepage

# Home route, renders home page and displays all recipes
@myapp_obj.route("/home")
@login_required  # Require the user to be logged in to access this page
def home():
    return render_template("home.html", title = "Home", pageClass = "home")  # Render home.html