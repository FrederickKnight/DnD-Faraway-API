import pytest
import os

from app import create_app

app = create_app()

#DB_TESTING_NAME = os.environ["DB_NAME"]

DB_TESTING_NAME = os.environ["DB_TESTING_NAME"]

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_TESTING_NAME}'
    with app.test_client() as client:
        yield client


