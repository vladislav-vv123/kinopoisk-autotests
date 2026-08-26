import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


@pytest.fixture(scope="session")
def api_token():
    return os.getenv("API_TOKEN")


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")


@pytest.fixture(scope="session")
def ui_url():
    return os.getenv("UI_URL")


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
