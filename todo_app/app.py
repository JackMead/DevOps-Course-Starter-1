from flask import Flask, render_template, request, redirect
import requests, json, os, datetime, operator, pymongo
from pymongo import mongo_client

from todo_app.flask_config import Config
from todo_app.data.todo_items import get_todo_cards, create_todo_card, move_todo_card, delete_todo_card, ToDoCard, ViewModel

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/')
    def index():
        alllistids = {'ToDo':'ToDo','Doing':'Doing','Done':'Done'}
        items = get_todo_cards()
        item_view_model = ViewModel(items, alllistids)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add_new', methods=['POST'])
    def addtolist():
        newitemtitle = request.form.get('title')
        newitemdescription = request.form.get('desc')
        create_todo_card(newitemtitle, newitemdescription)
        return redirect(request.headers.get('Referer'))

    @app.route('/update', methods=['POST'])
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
            if request.form.get("deletecheck_" + card.id) == card._id:
                delete_todo_card(card.id)
        return redirect(request.headers.get('Referer'))

    @app.route('/show_older_done_items', methods=['POST'])
    def show_older_completed_items():
        alllistids = {'ToDo':'ToDo','Doing':'Doing','Done':'Done'}
        items = get_todo_cards()
        item_view_model = ViewModel(items, alllistids)
        return render_template('showolderitems.html', view_model=item_view_model)
    

    if __name__ == '__main__':
        app.run()

    return app
