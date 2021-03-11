import requests, json, os, datetime

class TrelloCard:
    def __init__(self, id, name, idList, due, description, modified):
        self.id = id
        self.name = name
        self.idList = idList
        self.due = due
        self.description = description
        self.modified = modified

class ViewModel:
    def __init__(self, items, lists):
        self._items = items
        self._lists = lists
    @property
    def items(self):
        return self._items

    @property
    def lists(self):
        return self._lists

    @property
    def todo(self):
        items = []
        for item in self._items:
            if item.idList == self._lists['todo']:
                items.append(item)
        return items

    @property
    def doing(self):
        items = []
        for item in self._items:
            if item.idList == self._lists['doing']:
                items.append(item)
        return items

    @property
    def done(self):
        items = []
        for item in self._items:
            if item.idList == self._lists['done']:
                items.append(item)
        return items

    @property
    def done_today(self):
        items = []
        for item in self._items:
            modified_date = str(item.modified)
            completed_date = modified_date.split(" ")
            todays_date = datetime.date.today()
            if item.idList == self._lists['done'] and completed_date[0] == str(todays_date):
                items.append(item)
        return items

    @property
    def done_before_today(self):
        items = []
        for item in self._items:
            modified_date = str(item.modified)
            completed_date = modified_date.split(" ")
            todays_date = datetime.date.today()
            if item.idList == self._lists['done'] and completed_date[0] != str(todays_date):
                items.append(item)
        return items

def get_credential_key():
    cred_key = os.environ.get('KEY')
    return cred_key

def get_credential_token():
    cred_token = os.environ.get('TOKEN')
    return cred_token


def get_trello_board_id():
    trello_board_id = os.environ.get('BOARDID')

    return trello_board_id

def get_trello_cards():
    board_id = get_trello_board_id()
    getcardparams = {'key': get_credential_key(), 'token': get_credential_token()}
    cardresults = requests.get(f'https://api.trello.com/1/boards/{board_id}/cards', params=getcardparams)
    cards = cardresults.json()
    all_cards = []
    for c in cards:
        if c['due'] == None:
            duedate = "No Due Date Specified"
        else:
            duedate = datetime.datetime.strptime(str(c['due']), '%Y-%m-%dT%H:%M:%S.%fZ')
        item_modified_date = str(c['dateLastActivity'])
        split_modified_date_from_milliseconds = item_modified_date.split('.')
        modified_date = datetime.datetime.strptime(str(split_modified_date_from_milliseconds[0]), '%Y-%m-%dT%H:%M:%S')

        c = TrelloCard(c['id'], c['name'], c['idList'], duedate, c['desc'], modified_date)
        all_cards.append(c)

    return all_cards

def get_trello_cards_from_list(list):
    alllists = get_trello_lists()
    for l in alllists:
        if l['name'] == list:
            desired_list_id = l['id']
    getcardfromlistparams = {'key': get_credential_key(), 'token': get_credential_token()}
    cardfromlistresults = requests.get(f'https://api.trello.com/1/lists/{desired_list_id}/cards', params=getcardfromlistparams)
    cards = cardfromlistresults.json()
    list_cards = []
    for c in cards:
        if c['due'] == None:
            duedate = "No Due Date Specified"
        else:
            duedate = datetime.datetime.strptime(str(c['due']), '%Y-%m-%dT%H:%M:%S.%fZ')
        item_modified_date = str(c['dateLastActivity'])
        split_modified_date_from_milliseconds = item_modified_date.split('.')
        modified_date = datetime.datetime.strptime(str(split_modified_date_from_milliseconds[0]), '%Y-%m-%dT%H:%M:%S')

        c = TrelloCard(c['id'], c['name'], c['idList'], duedate, c['desc'], modified_date)
        list_cards.append(c)

    return list_cards

def get_trello_lists():
    board_id = get_trello_board_id()
    getlistparams = {'key': get_credential_key(), 'token': get_credential_token()}
    listresults = requests.get(f'https://api.trello.com/1/boards/{board_id}/lists', params=getlistparams)
    lists = listresults.json()

    return lists

def get_trello_list_id(list_name):
    alllists = get_trello_lists()
    for l in alllists:
        if l['name'] == list_name:
            desired_list_id = l['id']
    return desired_list_id

def create_new_trello_card(card_name, card_description):
    lists = get_trello_lists()
    duedate = str(datetime.datetime.today() + datetime.timedelta(days=30))
    split_item_duedate = duedate.split(".")
    newitemduedate = datetime.datetime.strptime(split_item_duedate[0], '%Y-%m-%d %H:%M:%S')
    for l in lists:
        if l['name'] == "To Do":
            desired_list_id = l['id']
    createcardparams = {'key': get_credential_key(), 'token': get_credential_token(), 'idList': desired_list_id, 'name': card_name, 'desc': card_description, 'due': str(newitemduedate)}
    requests.post('https://api.trello.com/1/cards', params=createcardparams)

def move_trello_card(card_id, new_list_id):
    movecardparams = {'key': get_credential_key(), 'token': get_credential_token(), 'idList': new_list_id}
    requests.put(f'https://api.trello.com/1/cards/{card_id}', params=movecardparams)

def delete_trello_card(card_id):
    deletecardparams = {'key': get_credential_key(), 'token': get_credential_token()}
    requests.delete(f'https://api.trello.com/1/cards/{card_id}', params=deletecardparams)