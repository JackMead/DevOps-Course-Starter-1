import requests
import json
import os

credkey = os.environ.get('KEY')
credtoken = os.environ.get('TOKEN')
board_id_config = os.environ.get('BOARDID')

class Trello_Card:
    def __init__(self, id, name, idList):
        self.id = id
        self.name = name
        self.idList = idList

def get_trello_board_id():
    trello_board_id = board_id_config

    return trello_board_id

def get_trello_cards():
    board_id = get_trello_board_id()
    getcardparams = {'key': credkey, 'token': credtoken}
    cardresults = requests.get(f'https://api.trello.com/1/boards/{board_id}/cards', params=getcardparams)
    cards = cardresults.json()
    all_cards = []
    for c in cards:
        c = Trello_Card(c['id'], c['name'], c['idList'])
        all_cards.append(c)

    return all_cards

def get_trello_lists():
    board_id = get_trello_board_id()
    getlistparams = {'key': credkey, 'token': credtoken}
    listresults = requests.get(f'https://api.trello.com/1/boards/{board_id}/lists', params=getlistparams)
    lists = listresults.json()

    return lists

def create_new_trello_card(card_name):
    lists = get_trello_lists()
    for l in lists:
        if l['name'] == "To Do":
            desired_list_id = l['id']
    createcardparams = {'key': credkey, 'token': credtoken, 'idList': desired_list_id, 'name': card_name}
    requests.post('https://api.trello.com/1/cards', params=createcardparams)

def move_trello_card(card_id, new_list_id):
    movecardparams = {'key': credkey, 'token': credtoken, 'idList': new_list_id}
    requests.put(f'https://api.trello.com/1/cards/{card_id}', params=movecardparams)