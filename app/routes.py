
from app import myapp_obj
from flask import render_template, redirect, request, flash
from app.forms import LoginForm, RegisterForm, RecipeForm, CommentForm
from app.models import User, Recipe, Comment
from app import db
from flask_login import current_user, login_required, login_user, logout_user

# All recipes tags route, renders home page and displays the page where you can select tags to see recipes.
@myapp_obj.route("/home/allrecipestagspage")
@login_required  # Ensure the user is logged in before accessing this route
def allrecipestags():
    recipes = Recipe.query.all();
    return render_template("allrecipestagspage.html", title = "All Recipes Tags", pageClass = "allrecipestagspage", recipes=recipes)  # Render home.html

# My recipes route, renders myrecipes page and displays all recipes
@myapp_obj.route("/home/myrecipes")
@login_required  # Ensure the user is logged in before accessing this route
def myrecipes():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all();
    return render_template("myrecipes.html", title = "My Recipes", pageClass = "myrecipes", recipes = recipes)  # Render home.html

# Following route, renders myrecipes page and displays all recipes
@myapp_obj.route("/home/following")
@login_required  # Ensure the user is logged in before accessing this route
def following():
    return render_template("following.html", title = "Following", pageClass = "following")  # Render home.html

# My profile route, renders myrecipes page and displays all recipes
@myapp_obj.route("/home/myprofile")
@login_required  # Ensure the user is logged in before accessing this route
def myprofile():
    return render_template("myprofile.html", title = "My Profile", pageClass = "myprofile")  # Render home.html

# Route when you click on your recipe, renders myrecipes page and displays all recipes
@myapp_obj.route("/home/myrecipes/mysinglerecipeview/<int:num>", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in before accessing this route
def mysinglerecipeview(num):
    recipe = Recipe.query.get(num)  # Fetch the recipe by its ID
    if recipe is None:  # If the recipe does not exist
        flash("Recipe not found.", "danger")  # Show a flash message
        return redirect("/home/myrecipes")  # Redirect to the recipes page
    # Form for comment
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(user_id = current_user.id,
                          recipe_id = num,
                          comment = form.comment.data)
        db.session.add(comment)
        db.session.commit()
        recipe.set_comment_ids(recipe.comment_ids + " " + str (comment.id))
        print(recipe.get_comment_ids())     # place holder for displaying comments

    # Format the ingredients and instructions
    formatted_ingredients = recipe.format_ingredients(recipe.ingredients)
    formatted_instructions = recipe.format_instructions(recipe.instructions)
    show_buttons = (current_user.is_authenticated and recipe.user_id == current_user.id)

    return render_template("mysinglerecipeview.html", title = "My Recipe", pageClass = "mysinglerecipeview",
                           ingredients=formatted_ingredients, instructions=formatted_instructions, recipe = recipe, show_buttons = show_buttons,
                           form = form, Comment = Comment, User = User)  # Render home.html

# Route when you click "add recipe" on "my recipes" page, renders myrecipes page and displays all recipes
@myapp_obj.route("/home/myrecipes/mysinglerecipeadd", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in before accessing this route
def mysinglerecipeadd():
    form = RecipeForm()
    if form.validate_on_submit(): # Checks if user input is valid
        # Creates a recipe
        recipe = Recipe(title=form.title.data,
                        user_id=current_user.id,
                        description=form.description.data,
                        ingredients=form.ingredients.data,
                        instructions=form.instructions.data,
                        )

        # Adds a recipe to the database
        db.session.add(recipe)
        db.session.commit()
        return redirect("/")
    else:
        # User has invalid input
        print("BAD INPUT")
    return render_template("mysinglerecipeadd.html", form=form, title = "Add A Recipe", pageClass = "mysinglerecipeadd")  # Render home.html
    # return render_template("test_add_recipe.html", form = form)

# Route currently has to be typed in to access the edit page
@myapp_obj.route("/home/myrecipes/mysinglerecipe/<int:recipe_id>/edit", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in before accessing this route
def mysinglerecipeedit(recipe_id):
    recipe_to_edit = Recipe.query.get(recipe_id)

    # Checks if user is the owner of the recipe
    if recipe_to_edit.user_id != current_user.id:
        flash("You do not have access to this recipe")
        return redirect("/")

    form = RecipeForm(obj = recipe_to_edit)
    if form.validate_on_submit(): # Checks if user input is valid
        # Edits a recipe
        recipe_to_edit.set_title(form.title.data)
        recipe_to_edit.set_description(form.description.data)
        recipe_to_edit.set_ingredients(form.ingredients.data)
        recipe_to_edit.set_instructions(form.instructions.data)

        return redirect("/")
    else:
        # User has invalid input
        print("BAD INPUT")


    return render_template("test_edit_recipe.html", form = form, recipe_to_edit=recipe_to_edit, title = "Edit A Recipe", pageClass = "mysinglerecipeedit")

# Route currently has to be typed in to access the edit page
@myapp_obj.route("/home/myrecipes/mysinglerecipe/<int:recipe_id>/delete", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in before accessing this route
def mysinglerecipedelete(recipe_id):
    recipe_to_edit = Recipe.query.get(recipe_id)

    # Checks if user is the owner of the recipe
    if recipe_to_edit.user_id != current_user.id:
        flash("You do not have access to this recipe")
        return redirect("/")

    db.session.delete(recipe_to_edit)   # Deletes Recipe
    db.session.commit()
    flash(f"{recipe_to_edit.get_title()} has been deleted")
    return redirect('/home/myrecipes')

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

