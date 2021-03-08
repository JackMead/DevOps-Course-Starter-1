from flask import Flask, render_template, request, redirect
import requests, json, os, datetime

from todo_app.flask_config import Config
from todo_app.data.trello_items import get_trello_board_id, get_trello_cards, get_trello_lists, create_new_trello_card, move_trello_card, ViewModel, get_trello_cards_from_list, get_trello_list_id, delete_trello_card

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
        alllistids = {'todo':get_trello_list_id('To Do'),'doing':get_trello_list_id('Doing'),'done':get_trello_list_id('Done')}
        items = get_trello_cards()
        item_view_model = ViewModel(items, alllistids)
        return render_template('index.html', view_model=item_view_model)

@app.route('/add_new', methods=['POST'])
def addtolist():
    newitemtitle = request.form.get('title')
    newitemdescription = request.form.get('desc')
    create_new_trello_card(newitemtitle, newitemdescription)
    return redirect(request.headers.get('Referer'))

@app.route('/update', methods=['POST'])
def movetolist():
    allcards = get_trello_cards()
    lists = get_trello_lists()
    for card in allcards:
        if request.form.get("inprogcheck_" + card.id) == card.id:
            for l in lists:
                if l['name'] == "Doing":
                    desired_list_id = l['id']
                    move_trello_card(card.id, desired_list_id)
        if request.form.get("donecheck_" + card.id) == card.id:
            for l in lists:
                if l['name'] == "Done":
                    desired_list_id = l['id']
                    move_trello_card(card.id, desired_list_id)
        if request.form.get("deletecheck_" + card.id) == card.id:
            delete_trello_card(card.id)
    return redirect(request.headers.get('Referer'))

@app.route('/show_older_done_items', methods=['POST'])
def show_older_completed_items():
    alllistids = {'todo':get_trello_list_id('To Do'),'doing':get_trello_list_id('Doing'),'done':get_trello_list_id('Done')}
    items = get_trello_cards()
    item_view_model = ViewModel(items, alllistids)
    return render_template('indextest.html', view_model=item_view_model)
   

if __name__ == '__main__':
    app.run()
