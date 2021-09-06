import pytest, os, json, pymongo, mongomock
from dotenv import find_dotenv, load_dotenv
from todo_app.data.todo_items import ToDoCard, ViewModel
import todo_app.app
from unittest.mock import patch, Mock

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    with mongomock.patch(servers=(('testmongo.com', 27017),)):
        test_app = todo_app.app.create_app()
        with test_app.test_client() as client:
            yield client

@patch('requests.get')
def test_index_page(client):
    response = client.get('/')

    assert b'To Do' in response.data
    assert b'Finish project' in response.data

@mongomock.patch(servers=(('testmongo.com', 27017),))
def test_add_item():
    db_connection = os.getenv('MDB_URL')
    db_name = os.getenv('MDB_DBNAME')
    connection = pymongo.MongoClient(db_connection)
    db = connection[db_name]
    item = {"name" : "test card"}
    collection = db['test_collection']
    collection.insert_one(item)
