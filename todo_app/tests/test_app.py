import pytest, datetime, os, json
from dotenv import find_dotenv, load_dotenv
from todo_app.data.trello_items import TrelloCard, ViewModel
import todo_app.app
from unittest.mock import patch, Mock

today = datetime.date.today()
dummy_cards = [
    TrelloCard(1,"Test Card 1",999,today,"Dummy Description 1",today - datetime.timedelta(days=8)),
    TrelloCard(2,"Test Card 2",998,today - datetime.timedelta(days=2),"Dummy Description 2", today - datetime.timedelta(days=7)),
    TrelloCard(3,"Test Card 3",997,today - datetime.timedelta(days=3),"Dummy Description 3", today - datetime.timedelta(days=6)),
    TrelloCard(4,"Test Card 4",999,today - datetime.timedelta(days=4),"Dummy Description 4", today),
    TrelloCard(5,"Test Card 5",999,today,"Dummy Description 5", today - datetime.timedelta(days=4)),
    TrelloCard(6,"Test Card 6",998,today - datetime.timedelta(days=6),"Dummy Description 6", today - datetime.timedelta(days=3)),
    TrelloCard(7,"Test Card 7",997,today - datetime.timedelta(days=7),"Dummy Description 7", today - datetime.timedelta(days=2)),
    TrelloCard(8,"Test Card 8",997,today - datetime.timedelta(days=8),"Dummy Description 8", today)
]

sample_trello_cards_response = dummy_cards


dummy_lists = [
    {
        "id": "123",
        "name": "To Do",
        "closed": False
    },
    {
        "id": "456",
        "name": "Doing",
        "closed": False
    },
    {
        "id": "789",
        "name": "Done",
        "closed": False
    }
]

sample_trello_lists_response = dummy_lists

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = todo_app.app.create_app()
    with test_app.test_client() as client:
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_requests
    response = client.get('/')
def mock_get_requests(url, params):
    BOARDID = os.environ.get('BOARDID')
    if url == f'https://api.trello.com/1/boards/{BOARDID}/lists':
        response = Mock()
        response.json.return_value = sample_trello_lists_response
        return response
    elif url == f'https://api.trello.com/1/boards/{BOARDID}/cards':
        response = Mock()
        response.json.return_value = sample_trello_cards_response
        return response
    return None
