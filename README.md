Welcome to Luke's To Do App...

# Mongo account set up

For this To Do App site to work, you will need to create a free Mongo account (https://www.mongodb.com/), and a database which has three collections called: 
- "To Do" (Items that you still need to start)
- "Doing" (Items that are currently in progress)
- "Done" (Items that have been completed)

You will need to create a MongoDB connection string account online and add the MONGO_DB_CONNECTION and MONGO_DB_NAME values into the .env file. The .env.template file has been updated to show the format required.

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

You can run the app using Docker containers. First, add any files that you do not want to copy to the container into the ".dockerignore" file, then build the latest image using the commands: 

Production image: `docker build --tag todo-app:production --target production .`
Development image: `docker build --tag todo-app:development --target development .`
Test image: `docker build --tag todo-app:test --target test .`

This uses the configuration in the "Dockerfile" in the root directory. You can then run a container that will serve the app by running:

Production image: `docker run -d -p 5000:5000 --env-file .env --mount type=bind,source="$(pwd)"/todo_app,target=/data/todo_app todo-app:production`
Development image: `docker run -d -p 5000:5000 --env-file .env --mount type=bind,source="$(pwd)"/todo_app,target=/data/todo_app todo-app:development`

# Navigating the app

This App will show you a list of all of your To Do items, categorised by their status (or list name), showing the item ID, name, description, due date, last modified date.

You can add new To Do items by adding typing the item name and description into the fields at the top and press the top "Add To-Do Item" button. This will add a new item with no due date into the "To Do" collection.

You can tick boxes to change the status of the item by ticking "Mark as In Progress", "Mark as Complete" or "Delete Item". The first two options will move the card to the 
correct collection and the "Delete Item" option will delete the card so that it is no longer in the MongoDB.

Items are shown as per their status. With the "Completed Items", if there are 5 or less completed items, all of those items will be shown regardless of status.
However, if there are more than 5, it will show you the items that have been marked as complete today. If you wish to view ALL of the completed items regardless
of the completion date, please click the "Show Older Completed Items" to view all.

# Testing the app

To test the app, install and run "poetry run pytest" in the root folder (above "todo_app" folder) and it will run through the tests specified in "tests" and "tests_e2e" folders. The tests in the "tests" folder will run tests on the functionailty of the app based on dummy data that is hard coded into the "test_config.py" file. Whereas the tests in the "tests_e2e" folder will test all functionality of the app. If all tests are successful, it means that the logic in the app is working correctly with the data from MongoDB. If there are failures, you will need to work out what it causing them. It is most likely going to be an issue with the set up/configuration of python/pytest/poetry, or the dummy data has been modified incorrectly.

To run a test individually, from the console, simply run "pytest test_config.py::*name_of_test_function*".

# Deploying the app

The application should deploy automatically via Travis CI from configuration in .travis.yml that will build the image via Docker Hub and push/release it via Heroku when a commit is pushed to the master git branch. To build/push/release the image manually via Docker Hub/Heroku, follow the steps below:

        # Build latest local Production image
        docker build --tag todo-app:production --target production .

        # Tag latest local Production image for Docker Hub
        docker tag todo-app:production lukeemcl/todo-production:latest

        # Push to Docker Hub
        docker push lukeemcl/todo-production:latest

        # Get the latest image from Docker Hub (built by your CI pipeline)
        $ docker pull lukeemcl/todo-production:latest

        # Tag it for Heroku
        $ docker tag lukeemcl/todo-production:latest registry.heroku.com/lwtodoapp-production/web

        # Push it to Heroku registry
        $ docker push registry.heroku.com/lwtodoapp-production/web

        # Login to Heroku
        heroku login

        # Login to the Heroku Container
        heroku container:login

        # Release the image via Heroku
        heroku container:release --app lwtodoapp-production web
        
        # Open app via browser
        heroku open --app lwtodoapp-production

        # View app logs if there is an issue
        heroku logs --tail --app lwtodoapp-production

