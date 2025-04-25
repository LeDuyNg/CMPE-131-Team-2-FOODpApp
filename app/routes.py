
from app import myapp_obj
from flask import render_template, redirect

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

# Route to log out, redirects to landing page
@myapp_obj.route("/logout")
def logout():
    return redirect("/");
