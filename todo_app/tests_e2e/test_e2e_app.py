import os, pytest
from threading import Thread
from todo_app.data.todo_items import create_test_db, delete_test_db
from todo_app import app
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from dotenv import find_dotenv,load_dotenv

@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    db_name = create_test_db('test_app')
    os.environ['MONGO_DB_NAME'] = db_name
    
    
    application = app.create_app()
    
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    thread.join(1)
    delete_test_db(db_name)

@pytest.fixture(scope="module")
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
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