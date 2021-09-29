from flask import Flask, render_template, request, redirect
import requests, json, os, datetime, operator, pymongo, flask_login, oauthlib
from pymongo import mongo_client
from flask_login import LoginManager, login_required, login_user, current_user
from oauthlib.oauth2 import WebApplicationClient

from todo_app.flask_config import Config
from todo_app.data.todo_items import get_todo_cards, create_todo_card, move_todo_card, delete_todo_card, ToDoCard, ViewModel
from todo_app.user import User

login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthenticated():
    github_client =  WebApplicationClient(os.environ.get('GHOAUTHCLIENTID'))
    github_redirect = github_client.prepare_request_uri("https://github.com/login/oauth/authorize")

    return redirect(github_redirect) 

@login_manager.user_loader
def load_user(github_user):
    
    return User(github_user)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = os.urandom(24)
    app.config['LOGIN_DISABLED'] = os.environ.get('LOGIN_DISABLED', 'False').lower() in ['true', '1']
    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        alllistids = {'ToDo':'ToDo','Doing':'Doing','Done':'Done'}
        items = get_todo_cards()
        item_view_model = ViewModel(items, alllistids)

        if hasattr('current_user', 'role'):
            if current_user.role == 'writer':
                return render_template('index.html', view_model=item_view_model)
            elif current_user.role == 'reader':
                return render_template('indexreadonly.html', view_model=item_view_model)
            else:
                return render_template('index.html', view_model=item_view_model)
        else:
            return render_template('index.html', view_model=item_view_model)


    @app.route('/add_new', methods=['POST'])
    @login_required
    def addtolist():
        newitemtitle = request.form.get('title')
        newitemdescription = request.form.get('desc')
        create_todo_card(newitemtitle, newitemdescription)
        return redirect(request.headers.get('Referer'))

    @app.route('/update', methods=['POST'])
    @login_required
    def movetolist():
        allcards = get_todo_cards()
        lists = {'ToDo':'ToDo','Doing':'Doing','Done':'Done'}
        for card in allcards:
            if request.form.get("inprogcheck_" + str(card.id)) == str(card.id):
                for l in lists:
                    if l == "Doing":
                        desired_list_id = l
                        move_todo_card(card.id, desired_list_id)
            if request.form.get("donecheck_" + str(card.id)) == str(card.id):
                for l in lists:
                    if l == "Done":
                        desired_list_id = l
                        move_todo_card(card.id, desired_list_id)
            if request.form.get("deletecheck_" + str(card.id)) == str(card.id):
                delete_todo_card(card.id)
        return redirect(request.headers.get('Referer'))

    @app.route('/show_older_done_items', methods=['POST'])
    @login_required
    def show_older_completed_items():
        alllistids = {'ToDo':'ToDo','Doing':'Doing','Done':'Done'}
        items = get_todo_cards()
        item_view_model = ViewModel(items, alllistids)
        return render_template('showolderitems.html', view_model=item_view_model)
    
    @app.route('/login/callback')
    def login_callback():
        callback_code = request.args.get("code")
        github_client =  WebApplicationClient(os.environ.get('GHOAUTHCLIENTID'))
        github_token = github_client.prepare_token_request("https://github.com/login/oauth/access_token", code=callback_code) 
        github_access = requests.post(github_token[0], headers=github_token[1], data=github_token[2], auth=(os.environ.get('GHOAUTHCLIENTID'), os.environ.get('GHOAUTHCLIENTSECRET')))
        github_json = github_client.parse_request_body_response(github_access.text)
        github_user_request_param = github_client.add_token("https://api.github.com/user")
        github_user = requests.get(github_user_request_param[0], headers=github_user_request_param[1]).json()
        
        login_user(User(github_user))

        return redirect('/') 

    if __name__ == '__main__':
        app.run()

    return app


