## <remove all of the example text and notes in < > such as this one>

## Functional Requirements
1. requirement <should be 1 sentence that describes requirement>
2. requirement
3. requirement
4. requirement
5. requirement
6. requirement
7. requirement
8. requirement
9. requirement
10. requirement
11. requirement
12. requirement
13. requirement
14. requirement

<using the syntax [](images/ui1.png) add images in a folder called images/ and place sketches of your webpages>

## Non-functional Requirements
1. non-functional
2. non-functional
## Use Cases <Le Duy Nguyen>

1. Use Case Name: User Registration

- **Pre-condition:** User is on the homepage.
- **Trigger:** User clicks on the **Register an Account** button.
- **Primary Sequence:**

    1. System displays a form for user to fill out to register for new account (fields: email, username, password).
    2. User fills out email field.
    3. System validates email address:
        - Must be a valid format.
        - Must be unique.
    4. User fills out username field.
    5. System validates username:
        - Must be unique.
    6. User fills out password field.
    7. System validates password:
        - Must be at least 8 characters.
    8. System creates a new user account.
    9. System notifies user that a new account has been successfully created.
    10. System stores new user information into database.
    11. System redirect the user to the homepage.

- **Primary Post-conditions:** A new user account is successfully stored into the database.
- **Alternate Sequence:**

    - **2a. User leaves email field empty:**

        - a. System displays an error message warning the user that the email field is empty.

        - b. System prompts user to enter email address.
    
    - **2b. User enters used email address:**

        - a. System displays an error message warning the user that this email address has been used.

        - b. System prompts user to enter a different email address.

    - **2c. User enters invalid email format:**

        - a. System displays an error message warning the user that the user entered an invalid email format.

        - b. System prompts user to enter a different email address.
        
    - **5a. User leaves username field empty:**

        - a. System displays an error message warning the user that the username field is empty.

         - b. System prompts user to enter username.
    
    - **5b. User enters used username:**

        - a. System displays an error message warning the user that this username has been used.

        - b. System prompts user to enter a different username.

    - **7a. User leaves the password field empty:**

        - a. System displays an error message warning the user that the password field is empty.

         - b. System prompts user to enter password.

    - **7b. User enters a password with less than 8 characters:**

        - a. System displays an error message warning the user that the password is too short.

        - b. System prompts user to enter a different password.
    ---
2. Use Case Name: User Login
- **Pre-condition:** User is on the homepage.
- **Trigger:** User clicks on the **Log In** button.
- **Primary Sequence:**
    1. System prompts user to enter email address.
    2. User enters email address.
    3. System validates email address:
        - Must be in a valid format.
        - Must match an existing account.
    4. System prompts user to enter password.
    5. System validates password:
        - Must match the stored password for the given email.
    6. System logs the user in.
    7. System redirect user to homepage.

- **Primary Post-conditions:** User is successfully logged in and redirected to homepage.
- **Alternate Sequence:**
    - **3a. User enters email in invalid format:**

        - a. System displays an error message warning the user that the user entered an invalid email format.

        - b. System prompts user to enter email again.

    - **3b. User enters an email not found in system:**

        - a. System displays an error message warning the user that the user the account doesn't exist.

        - b. System offers option to retry or register a new account.

    - **6a. User enters incorrect password:**

        - a. System displays an error message warning the user that the password is incorrect.

        - b. System prompts the user to retry or reset password.
    ---
3. Use Case Name: User Logout
- **Pre-condition:** User is logged in.
- **Trigger:** User clicks on **Log Out** button.
- **Primary Sequence:**
    1. System displays a message indicating the user is about to log out.
    2. System prompts user with 2 options:
        - **Cancel**: Cancel the logout process.
        - **Confirm**: Proceed with logging out.
    3. User clicks **Confirm**.
    5. System logs user out.
    6. System clears user session.
    7. System redirects user homepage.
    8. System displays a message confirming successfully logout.

- **Primary Post-conditions:** User session is terminated, and the user is redirected to the homepage.
- **Alternate Sequence:** 
    - **3a. User clicks "Cancel":**

        - a. System aborts logout process.

        - b. System keeps the user logged in and returns to current view.
    ---
4. Use Case Name: Create Recipe
- **Pre-condition:** User is logged in.
- **Trigger:** User clicks on **Add Recipe** button.
- **Primary Sequence:**
    1. System prompts user to enter title of new recipe.
    2. User enters title.
    3. System prompts user to enter description of new recipe.
    4. User enters description.
    5. System prompts user to enter a list of ingredients of new recipe (comma separated).
    6. User enters ingredients.
    7. System prompts user to enter a list of instructions of new recipe (comma separated).
    8. User enters instructions.
    9. System stores new recipe to database.
    10. System redirect user to newly created recipe's detail page.

- **Primary Post-conditions:** A new recipe is stored into the database and viewable on its detail page.
- **Alternate Sequence:**
    - **2a. User leaves title field empty:**
        - a. System displays an error message warning the user that title field is empty.

        - b. System prompts user to enter title.

    - **6a. User leaves ingredients field empty:**
        - a. System displays an error message warning the user that at least one ingredient is required.

        - b. System prompts user to enter ingredients.

    - **8a. User leaves instructions field empty:**
        - a. System displays an error message warning the user that at least one instruction is required.

        - b. System prompts user to enter instructions.
    ---
5. Use Case Name: Edit recipe
- **Pre-condition:** 
    - User is logged in.
    - User is on a the detail page of the recipe to edit.
    - User is the owner of the recipe.
- **Trigger:** User clicks on **Edit Recipe** button.
- **Primary Sequence:**
    1. System loads the existing recipe into an editable form (fields: title, description, ingredients, instructions).
    2. User edits one or more fields.
    3. User submits the updates recipe.
    4. System validates the updates fields:
        - Title, ingredients, instructions must not be empty.
    5. System saves the updated recipe into the database.
    6. System redirects user to the updated recipe's detail page.
    7. System displays a confirmation message indicating the recipe has been successfully updated.

- **Primary Post-conditions:** The recipe is updated and viewable in its detail page.
- **Alternate Sequence:**
    - **3a. User cancels the edit:**
        - a. System discards the changes.
        - b. System redirects user back to the recipe detail page without saving changes.

    - **4a. User leaves one of the required fields empty:**
        - a. System displays an error message warning the user the specific field(s) are empty.

        - b. System prompts user to enter the missing field(s).
    ---
6. Use Case Name: Delete Recipe
- **Pre-condition:**     
    - User is logged in.
    - User is on a the detail page of the recipe to delete.
    - User is the owner of the recipe.
- **Trigger:** User clicks on **Delete Recipe** button.
- **Primary Sequence:**
    1. System displays a confirmation prompt asking the user to confirm deletion.
    2. User clicks **Confirm**.
    3. System deletes the recipe from the database.
    4. System redirects user to their list of recipes.
    5. System displays a confirmation message indicating the recipe has been successfully deleted.

- **Primary Post-conditions:** The recipe is permanently deleted from the database and no longer viewable by any users.
- **Alternate Sequence:**
    - **2a. User clicks "Cancel":**
        - a. System aborts the deletion process.
        - System keeps the user on recipe detail page.
---


