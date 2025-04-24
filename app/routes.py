
from app import myapp_obj
from flask import render_template

# Login route (landing page), renders home page and displays all recipes
@myapp_obj.route("/")
def login():
    return render_template("login.html", title = "Log In", pageClass = "login")  # Render home.html

# Register route, renders home page and displays all recipes
@myapp_obj.route("/register")
def register():
    return render_template("register.html", title = "Register", pageClass = "register")  # Render home.html


# Home route, renders home page and displays all recipes
@myapp_obj.route("/home")
def home():
    return render_template("home.html", title = "Home", pageClass = "home")  # Render home.html
