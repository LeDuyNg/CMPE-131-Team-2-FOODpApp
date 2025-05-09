
from app import myapp_obj
from flask import render_template, redirect, request, flash, url_for
from app.forms import LoginForm, RegisterForm, RecipeForm, UpdateForm, CommentForm, RatingForm
from app.models import User, Recipe, Comment
from app import db
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func, or_
import random
from datetime import date
import requests

# All recipes tags route, renders home page and displays the page where you can select tags to see recipes.
@myapp_obj.route("/home/allrecipestagspage", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in before accessing this route
def allrecipestags():
    form = RecipeForm()
    if request.method == 'POST':
        args = {}
        if form.title_for_search.data != "":
            args["title"] = form.title_for_search.data

        if form.temperature.data != "":
            args["temperature"] = form.temperature.data

        if form.dish_type.data != "":
            args["dish_type"] = form.dish_type.data

        if form.dairy.data != "":
            args["dairy"] = form.dairy.data

        if form.sweetness.data != "":
            args["sweetness"] = form.sweetness.data

        if form.meat.data != "":
            args["meat"] = form.meat.data

        if form.seafood.data != "":
            args["seafood"] = form.seafood.data

        url = url_for("allrecipestags", **args)
        return redirect(url)


    query = Recipe.query

    if ("title" in request.args):
        arg = request.args.get("title")
        form.title_for_search.data = arg
        query = query.filter(or_(Recipe.ingredients.icontains(arg), Recipe.title.icontains(arg)))

    if ("temperature" in request.args):
        arg = request.args.get("temperature")
        form.temperature.data = arg
        query = query.filter(func.json_extract(Recipe.tags, "$.temperature") == arg)

    if ("dish_type" in request.args):
        arg = request.args.get("dish_type")
        form.dish_type.data = arg
        query = query.filter(func.json_extract(Recipe.tags, "$.dish_type") == arg)

    if ("dairy" in request.args):
        arg = request.args.get("dairy")
        form.dairy.data = arg
        query = query.filter(func.json_extract(Recipe.tags, "$.dairy") == arg)

    if ("sweetness" in request.args):
        arg = request.args.get("sweetness")
        form.sweetness.data = arg
        query = query.filter(func.json_extract(Recipe.tags, "$.sweetness") == arg)

    if ("meat" in request.args):
        arg = request.args.get("meat")
        form.meat.data = arg
        query = query.filter(func.json_extract(Recipe.tags, "$.meat") == arg)

    if ("seafood" in request.args):
        arg = request.args.get("seafood")
        form.seafood.data = arg
        query = query.filter(func.json_extract(Recipe.tags, "$.seafood") == arg)


    #tags["temperature"] = form.temperature.data
    #    tags["dish_type"] = form.dish_type.data
    #    tags["dairy"] = form.dairy.data
    #    tags["sweetness"] = form.sweetness.data
    #    tags["meat"] = form.meat.data
    #    tags["seafood"] = form.seafood.data

    recipes = query.all()
    return render_template("allrecipestagspage.html", title = "All Recipes Tags", form = form, pageClass = "allrecipestagspage", recipes=recipes)  # Render home.html

# My recipes route, renders myrecipes page and displays all recipes
@myapp_obj.route("/home/myrecipes")
@login_required  # Ensure the user is logged in before accessing this route
def myrecipes():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
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

    comment_form = CommentForm()
    rating_form = RatingForm()

    if comment_form.validate_on_submit():
        comment = Comment(user_id = current_user.id,
                          recipe_id = num,
                          comment = comment_form.comment.data)
        db.session.add(comment)
        db.session.commit()
        recipe.add_comment_id(comment.id)

    if rating_form.validate_on_submit():
        recipe.rate_recipe(current_user.id, rating_form.rating.data)

    # Format the ingredients and instructions
    formatted_ingredients = recipe.format_ingredients(recipe.ingredients)
    formatted_instructions = recipe.format_instructions(recipe.instructions)

    # Check to see if user is the owner of recipe
    show_buttons = (current_user.is_authenticated and recipe.user_id == current_user.id)

    # Check if recipe is in user's favorite
    check_favorite = (recipe in current_user.favorite_recipes.all() )

    comment_list = recipe.get_comment_list()


    return render_template("mysinglerecipeview.html", title = "My Recipe", pageClass = "mysinglerecipeview",
                           ingredients=formatted_ingredients, instructions=formatted_instructions, recipe = recipe, show_buttons = show_buttons,
                           comment_form = comment_form, comment_list = comment_list, rating_form = rating_form, check_favorite = check_favorite)  # Render home.html

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

        tags = {}
        tags["temperature"] = form.temperature.data
        tags["dish_type"] = form.dish_type.data
        tags["dairy"] = form.dairy.data
        tags["sweetness"] = form.sweetness.data
        tags["meat"] = form.meat.data
        tags["seafood"] = form.seafood.data

        recipe.set_tags(tags)

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

        tags = {}
        tags["temperature"] = form.temperature.data
        tags["dish_type"] = form.dish_type.data
        tags["dairy"] = form.dairy.data
        tags["sweetness"] = form.sweetness.data
        tags["meat"] = form.meat.data
        tags["seafood"] = form.seafood.data

        recipe_to_edit.set_tags(tags)

        return redirect("/")

    tags = recipe_to_edit.tags

    if ("temperature" in tags):
        form.temperature.data = tags["temperature"]

    if ("dish_type" in tags):
        form.dish_type.data = tags["dish_type"]

    if ("dairy" in tags):
        form.dairy.data = tags["dairy"]

    if ("sweetness" in tags):
        form.sweetness.data = tags["sweetness"]

    if ("meat" in tags):
        form.meat.data = tags["meat"]

    if ("seafood" in tags):
        form.seafood.data = tags["seafood"]


    return render_template("test_edit_recipe.html", form = form, recipe_to_edit=recipe_to_edit, title = "Edit A Recipe", pageClass = "mysinglerecipeedit", tags = tags)


@myapp_obj.route("/home/myrecipes/mysinglerecipe/<int:recipe_id>/delete", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in before accessing this route
def mysinglerecipedelete(recipe_id):
    recipe_to_edit = Recipe.query.get(recipe_id)

    # Checks if user is the owner of the recipe
    if recipe_to_edit.user_id != current_user.id:
        flash("You do not have access to this recipe")
        return redirect("/")

    recipe_to_edit.delete_all_comments()
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
    recipes = Recipe.query.all()
    # derive an integer seed from today’s date
    today = date.today()
    seed = today.toordinal()
    random.seed(seed)
    if recipes:
        random_recipe = random.choice(recipes)
    else:
        random_recipe = Recipe(title = "", description = "", ingredients = "", instructions = "", id = -1)

    return render_template("home.html", title = "Home", pageClass = "home", recipe = random_recipe)  # Render home.html

@myapp_obj.route("/home/random_recipe")
@login_required
def get_random_recipe():
    food_url = "https://www.themealdb.com/api/json/v1/1/random.php"
    food_response = requests.get(food_url)
    food_data = food_response.json()
    meal = food_data['meals'][0]
    return render_template('food.html', meal=meal)

@myapp_obj.route("/home/myrecipes/mysinglerecipeadd/<string:meal_id>", methods=['GET', 'POST'])
@login_required
def add_API_recipe(meal_id):
    # Call the API to retrieve the recipe using its id
    food_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    food_response = requests.get(food_url)
    food_data = food_response.json()
    meal = food_data['meals'][0]

    # Data handling
    ingredient_entries = []

    for index in range(1, 21):
        # Oull the ingredient name and its measure
        ingredient_name    = meal.get(f"strIngredient{index}")
        ingredient_amount  = meal.get(f"strMeasure{index}")

        # Only include entries where the ingredient name is present and not whitespace
        if ingredient_name and ingredient_name.strip():
            # Combine amount and name into one line, omit the amount if it is missing
            line = f"{ingredient_amount or ''} {ingredient_name}".strip()
            ingredient_entries.append(line)

    
    initial = {
        'title'       : meal['strMeal'],
        'description' : meal['strCategory'] + " – " + meal['strArea'],  # or however you like
        'ingredients' : "\n".join(ingredient_entries),
        'instructions': meal['strInstructions'],
    }

    form = RecipeForm(data=initial)
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

        tags = {}
        tags["temperature"] = form.temperature.data
        tags["dish_type"] = form.dish_type.data
        tags["dairy"] = form.dairy.data
        tags["sweetness"] = form.sweetness.data
        tags["meat"] = form.meat.data
        tags["seafood"] = form.seafood.data

        recipe.set_tags(tags)

        return redirect("/")
    else:
        # User has invalid input
        print("BAD INPUT")
    return render_template("add_API_recipe.html", form=form, title = "Add A Recipe", pageClass = "mysinglerecipeadd")

@myapp_obj.route("/home/myprofile/update", methods=['GET', 'POST'])
@login_required
def update_profile():
    user = User.query.get(current_user.id)
    form = UpdateForm(obj = user)
    if form.validate_on_submit():
        user.update_email(email = form.email.data)
        user.update_username(username = form.username.data)
        user.set_password(password = form.password.data)
        db.session.commit()
        return redirect("/home/myprofile")
    return render_template("test_edit_profile.html", title = "Update profile", pageClass = "update", user = user, form = form)

@myapp_obj.route("/home/myrecipes/mysinglerecipe/<int:recipe_id>/add_favorite", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in before accessing this route
def add_favorite(recipe_id):
    user = User.query.get(current_user.id)
    favorite_recipe = Recipe.query.get(recipe_id)
    user.add_favorite(favorite_recipe)
    return redirect(url_for('mysinglerecipeview', num = recipe_id))

@myapp_obj.route("/home/myrecipes/mysinglerecipe/<int:recipe_id>/remove_favorite", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in before accessing this route
def remove_favorite(recipe_id):
    user = User.query.get(current_user.id)
    favorite_recipe = Recipe.query.get(recipe_id)
    user.remove_favorite(favorite_recipe)
    print("in here")
    return redirect(url_for('my_favorites'))

@myapp_obj.route("/home/myprofile/deleteprofile")
@login_required
def delete_profile():
    user = User.query.get(current_user.id)                                      # Find me
    user_recipes = Recipe.query.filter_by(user_id=current_user.id).all()        # Find my recipes
    for recipe in user_recipes:
        recipe.delete_all_comments()    # Delete all comments in my recipes
        db.session.delete(recipe)       # Delete my recipe

    user_comments = Comment.query.filter_by(user_id = current_user.id).all()    # Find my comments
    for comment in user_comments:
        comment.delete()                  # Delete my comment
    db.session.delete(user)               # Delete me
    db.session.commit()
    return redirect(url_for('logout'))

@myapp_obj.route("/home/myprofile/favorites")
@login_required
def my_favorites():
    recipes = current_user.favorite_recipes.all()
    
    return render_template('favorites.html', recipes=recipes, title = "My Favorite Recipes", pageClass = "myrecipes")