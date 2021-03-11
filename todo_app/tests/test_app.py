import pytest, datetime, os, json
from dotenv import find_dotenv, load_dotenv
from todo_app.data.trello_items import TrelloCard, ViewModel
import todo_app.app
from unittest.mock import patch, Mock

today = datetime.date.today()
dummy_cards = [
    {
        "id": "1",
        "checkItemStates": None,
        "closed": False,
        "dateLastActivity": "2021-03-04T16:46:45.995Z",
        "desc": "testing desc",
        "descData": None,
        "dueReminder": None,
        "idBoard": "123456ZYXWV",
        "idList": "999",
        "idMembersVoted": [],
        "idShort": 26,
        "idAttachmentCover": None,
        "idLabels": [],
        "manualCoverAttachment": False,
        "name": "Test Card 1",
        "pos": 16384,
        "shortLink": "hDebNQN6",
        "isTemplate": False,
        "cardRole": None,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": False,
            "votes": 0,
            "viewingMemberVoted": False,
            "subscribed": False,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": None,
            "comments": 0,
            "attachments": 0,
            "description": True,
            "due": "2021-04-03T20:46:45.000Z",
            "dueComplete": False,
            "start": None
        },
        "dueComplete": False,
        "due": "2021-04-03T20:46:45.000Z",
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/hDebNQN6",
        "start": None,
        "subscribed": False,
        "url": "https://trello.com/c/hDebNQN6/26-finish-project",
        "cover": {
            "idAttachment": None,
            "color": None,
            "idUploadedBackground": None,
            "size": "normal",
            "brightness": "light",
            "idPlugin": None
        }
    },
     {
        "id": "1",
        "checkItemStates": None,
        "closed": False,
        "dateLastActivity": "2021-03-04T16:46:45.995Z",
        "desc": "testing desc",
        "descData": None,
        "dueReminder": None,
        "idBoard": "123456ZYXWV",
        "idList": "998",
        "idMembersVoted": [],
        "idShort": 26,
        "idAttachmentCover": None,
        "idLabels": [],
        "manualCoverAttachment": False,
        "name": "Test Card 2",
        "pos": 16384,
        "shortLink": "hDebNQN6",
        "isTemplate": False,
        "cardRole": None,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": False,
            "votes": 0,
            "viewingMemberVoted": False,
            "subscribed": False,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": None,
            "comments": 0,
            "attachments": 0,
            "description": True,
            "due": "2021-04-03T20:46:45.000Z",
            "dueComplete": False,
            "start": None
        },
        "dueComplete": False,
        "due": "2021-04-03T20:46:45.000Z",
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/hDebNQN6",
        "start": None,
        "subscribed": False,
        "url": "https://trello.com/c/hDebNQN6/26-finish-project",
        "cover": {
            "idAttachment": None,
            "color": None,
            "idUploadedBackground": None,
            "size": "normal",
            "brightness": "light",
            "idPlugin": None
        }
    },
     {
        "id": "1",
        "checkItemStates": None,
        "closed": False,
        "dateLastActivity": "2021-03-04T16:46:45.995Z",
        "desc": "testing desc",
        "descData": None,
        "dueReminder": None,
        "idBoard": "123456ZYXWV",
        "idList": "997",
        "idMembersVoted": [],
        "idShort": 26,
        "idAttachmentCover": None,
        "idLabels": [],
        "manualCoverAttachment": False,
        "name": "Test Card 3",
        "pos": 16384,
        "shortLink": "hDebNQN6",
        "isTemplate": False,
        "cardRole": None,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": False,
            "votes": 0,
            "viewingMemberVoted": False,
            "subscribed": False,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": None,
            "comments": 0,
            "attachments": 0,
            "description": True,
            "due": "2021-04-03T20:46:45.000Z",
            "dueComplete": False,
            "start": None
        },
        "dueComplete": False,
        "due": "2021-04-03T20:46:45.000Z",
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/hDebNQN6",
        "start": None,
        "subscribed": False,
        "url": "https://trello.com/c/hDebNQN6/26-finish-project",
        "cover": {
            "idAttachment": None,
            "color": None,
            "idUploadedBackground": None,
            "size": "normal",
            "brightness": "light",
            "idPlugin": None
        }
    }
]

sample_trello_cards_response = dummy_cards


dummy_lists = [
    {
        "id": 999,
        "name": "To Do",
        "closed": False
    },
    {
        "id": 998,
        "name": "Doing",
        "closed": False
    },
    {
        "id": 997,
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
    mock_get_requests.side_effect = mock_trello_api
    response = client.get('/')
def mock_trello_api(url, params):
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
