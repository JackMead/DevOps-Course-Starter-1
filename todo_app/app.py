from flask import Flask, render_template, request, redirect
from operator import itemgetter
import requests
import json
import os

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, get_item, add_item, save_item, remove_item
from todo_app.data.trello_items import get_trello_board_id, get_trello_cards, get_trello_lists, create_new_trello_card, move_trello_card

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    #items = sorted(get_items(), key=itemgetter('status'), reverse=True)
    alllists = get_trello_lists()
    items = get_trello_cards()
    return render_template("index.html",items=items, lists=alllists)

@app.route('/add_new', methods=['POST'])
def addtolist():
    newitemtitle = request.form.get('title')
    create_new_trello_card(newitemtitle)
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
    return redirect(request.headers.get('Referer'))
   

if __name__ == '__main__':
    app.run()
