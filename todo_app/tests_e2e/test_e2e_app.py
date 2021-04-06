import os, pytest
from threading import Thread
from todo_app.data.trello_items import create_trello_board, delete_trello_board
from todo_app import app
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from dotenv import find_dotenv,load_dotenv

@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    board_id = create_trello_board("TestBoard")
    os.environ['BOARDID'] = board_id
    
    
    application = app.create_app()
    
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    thread.join(1)
    delete_trello_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe") as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://127.0.0.1:5000/')
    assert driver.title == 'To-Do App'

    driver.find_element_by_name("title").send_keys('Test Name')
    driver.find_element_by_name("desc").send_keys('Test Description')
    driver.find_element_by_name("addnew").click()

    assert driver.find_element_by_xpath("//*[starts-with(@id, 'ToDo_')]")
    driver.find_element_by_xpath("//*[starts-with(@name, 'inprogcheck_')]").click()
    driver.find_element_by_xpath("//*[starts-with(@id, 'submit')]").click()

    assert driver.find_element_by_xpath("//*[starts-with(@id, 'Doing_')]")
    driver.find_element_by_xpath("//*[starts-with(@name, 'donecheck_')]").click()
    driver.find_element_by_xpath("//*[starts-with(@id, 'submit')]").click()