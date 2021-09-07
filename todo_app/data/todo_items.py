from pymongo import mongo_client
import requests, json, os, datetime, pymongo

class ToDoCard:
    def __init__(self, id, name, idList, due, description, modified):
        self.id = id
        self.name = name
        self.idList = idList
        self.due = due
        self.description = description
        self.modified = modified
    
    def get_card_as_dictionary(self):
        return {'name' : self.name, 'idList' : self.idList, 'due_date' : self.due_date, 'description' : self.description, 'modified' : self.modified}

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
            if item.idList == self._lists['ToDo']:
                items.append(item)
        return items

    @property
    def doing(self):
        items = []
        for item in self._items:
            if item.idList == self._lists['Doing']:
                items.append(item)
        return items

    @property
    def done(self):
        items = []
        for item in self._items:
            if item.idList == self._lists['Done']:
                items.append(item)
        return items

    @property
    def done_today(self):
        items = []
        for item in self._items:
            modified_date = str(item.modified)
            completed_date = modified_date.split(" ")
            todays_date = datetime.date.today()
            if item.idList == self._lists['Done'] and completed_date[0] == str(todays_date):
                items.append(item)
        return items

    @property
    def done_before_today(self):
        items = []
        for item in self._items:
            modified_date = str(item.modified)
            completed_date = modified_date.split(" ")
            todays_date = datetime.date.today()
            if item.idList == self._lists['Done'] and completed_date[0] != str(todays_date):
                items.append(item)
        return items

def get_mongodb_url():
    mongodb_url = os.environ.get('MONGO_DB_CONNECTION')
    return mongodb_url

def connect_mongodb():
    mongodb_url = get_mongodb_url()
    mongo_client = pymongo.MongoClient(mongodb_url)
    db_name = os.environ.get('MONGO_DB_NAME')
    db = mongo_client[db_name]
    return db

def get_todo_cards():
    db = connect_mongodb()
    collections = db.list_collection_names()
    
    all_cards = []
    for c in collections:
        collection = db[c]
        for card in collection.find({}):
            all_cards.append(ToDoCard(card['_id'], card['name'], card['idList'], card['due_date'], card['description'], card['modified']))
            
    return all_cards

def create_todo_card(new_card):
    db = connect_mongodb()
    card = new_card.get_card_as_dictionary()
    db['ToDo'].insert_one(card)

def move_todo_card(card_id, new_list_id):
    db = connect_mongodb()
    collections = db.list_collection_names()

    for c in collections:
        collection = db[c]
        for card in collection.find({}): 
            if str(card['_id']) == str(card_id):
                new_card = ToDoCard(0, card['name'], new_list_id, card['due_date'], card['description'], datetime.datetime.today())
                new_collection = db[new_list_id]
                new_collection.insert_one(new_card.get_card_as_dictionary())
                result = collection.delete_one({'_id' : card['_id']})
                print(result)
                break

def create_test_db(db_name):
    db_connection = get_mongodb_url()
    mongo_client = pymongo.MongoClient(db_connection)
    db = mongo_client[db_name]
    db['ToDo']
    db['Doing']
    db['Done']

    return db_name

def delete_test_db(db_name):
    db_connection = get_mongodb_url()
    mongo_client = pymongo.MongoClient(db_connection)
    mongo_client.drop_database(db_name)