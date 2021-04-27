Welcome to Luke's To Do App...

# Trello account set up

For this To Do App site to work, you will need to create a Trello account (http://trello.com), and a Trello board which has three lists called (Default): 
- "To Do" (Items that you still need to start)
- "Doing" (Items that are currently in progress)
- "Done" (Items that have been completed)

You will need to create a Trello API key from your account online (follow this guide: https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction) and add the KEY and TOKEN values into the .env file. Once you have done this, you can use Postman (or other) to query the API (using the KEY and TOKEN for authentication) to get your BOARDID. Once you have this, you will need to add this into the BOARDID value
in the .env file as well. The .env.template file has been updated to show the format required.

# Setting up the app

        # System Requirements

        The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

        # Poetry installation (Bash)

        ```bash
        curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
        ```

        # Poetry installation (PowerShell)

        ```powershell
        (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
        ```

        # Dependencies

        The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

        ```bash
        $ poetry install
        ```

        You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

        ```bash
        $ cp .env.template .env  # (first time only)
        ```

        The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

        # Running the App

        Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
        ```bash
        $ poetry run flask run
        ```

        You should see output similar to the following:
        ```bash
        * Serving Flask app "app" (lazy loading)
        * Environment: development
        * Debug mode: on
        * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
        * Restarting with fsevents reloader
        * Debugger is active!
        * Debugger PIN: 226-556-590
        ```
        Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.'''

# Starting the app

You can run the app using Vagrant. Run the command "vagrant up" in the terminal to build a VM to run the application. You can then access the app through the browser at "http://localhost:5000".

# Navigating the app

This App will show you a list of all of your To Do items, categorised by their status (or list name), showing the item ID, name, description, due date, last modified date.

You can add new To Do items by adding typing the item name and description into the fields at the top and press the top "Add To-Do Item" button. This will add a new item
via the Trello API with no due date into the "To Do" list.

You can tick boxes to change the status of the item by ticking "Mark as In Progress", "Mark as Complete" or "Archive". The first two options will move the card to the 
correct list and the "Archive" option will archive the item so that it is no longer visible as an active item in Trello.

Items are shown as per their status. With the "Completed Items", if there are 5 or less completed items, all of those items will be shown regardless of status.
However, if there are more than 5, it will show you the items that have been marked as complete today. If you wish to view ALL of the completed items regardless
of the completion date, please click the "Show Older Completed Items" to view all.

# Testing the app

To test the app, install and run "poetry run pytest" in the root folder (above "todo_app" folder) and it will run through the tests specified in "tests" and "tests_e2e" folders. The tests in the "tests" folder will run tests on the functionailty of the app based on dummy data that is hard coded into the "test_config.py" file. Whereas the tests in the "tests_e2e" folder will test all functionality of the app. If all tests are successful, it means that the logic in the app is working correctly with the data from Trello. If there are failures, you will need to work out what it causing them. It is most likely going to be an issue with the set up/configuration of python/pytest/poetry, or the dummy data has been modified incorrectly.

To run a test individually, from the console, simply run "pytest test_config.py::*name_of_test_function*".

