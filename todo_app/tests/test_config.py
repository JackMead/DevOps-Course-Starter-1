import pytest, datetime
from todo_app.data.todo_items import ViewModel, ToDoCard


@pytest.fixture
def dummy_card_list():
    today = datetime.date.today()
    all_cards = [
        ToDoCard(1,"Test Card 1",999,today,"Dummy Description 1",today - datetime.timedelta(days=8)),
        ToDoCard(2,"Test Card 2",998,today - datetime.timedelta(days=2),"Dummy Description 2", today - datetime.timedelta(days=7)),
        ToDoCard(3,"Test Card 3",997,today - datetime.timedelta(days=3),"Dummy Description 3", today - datetime.timedelta(days=6)),
        ToDoCard(4,"Test Card 4",999,today - datetime.timedelta(days=4),"Dummy Description 4", today),
        ToDoCard(5,"Test Card 5",999,today,"Dummy Description 5", today - datetime.timedelta(days=4)),
        ToDoCard(6,"Test Card 6",998,today - datetime.timedelta(days=6),"Dummy Description 6", today - datetime.timedelta(days=3)),
        ToDoCard(7,"Test Card 7",997,today - datetime.timedelta(days=7),"Dummy Description 7", today - datetime.timedelta(days=2)),
        ToDoCard(8,"Test Card 8",997,today - datetime.timedelta(days=8),"Dummy Description 8", today)
    ]
    return all_cards

@pytest.fixture
def list_ids():
    trello_list_ids = {"todo": 999, "doing": 998, "done": 997}
    return trello_list_ids

class TestTrello():

    @staticmethod
    def test_todo_items(dummy_card_list, list_ids):
        todo_list_id = list_ids['todo']
        view_model = ViewModel(dummy_card_list, list_ids)
        
        all_todo_items = view_model.todo

        for card in all_todo_items:
            assert card.idList == todo_list_id

    @staticmethod
    def test_doing_items(dummy_card_list, list_ids):
        doing_list_id = list_ids['doing']
        view_model = ViewModel(dummy_card_list, list_ids)
        
        all_doing_items = view_model.doing

        for card in all_doing_items:
            assert card.idList == doing_list_id

    @staticmethod
    def test_all_done_items(dummy_card_list, list_ids):
        done_list_id = list_ids['done']
        view_model = ViewModel(dummy_card_list, list_ids)
        
        all_done_items = view_model.done

        for card in all_done_items:
            assert card.idList == done_list_id

    @staticmethod
    def test_recent_done_items(dummy_card_list, list_ids):
        view_model = ViewModel(dummy_card_list, list_ids)
        items_done_today = view_model.done_today
        assert len(items_done_today) == 1

    @staticmethod
    def test_older_done_items(dummy_card_list, list_ids):
        view_model = ViewModel(dummy_card_list, list_ids)
        items_done_before_today = view_model.done_before_today
        assert len(items_done_before_today) == 2

