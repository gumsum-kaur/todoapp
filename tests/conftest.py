
import os
import tempfile
import pytest
from todo_app.app import app
from todo_app.database import init_db

@pytest.fixture
def client():
    # Create a temp file for the DB for this test
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd) 

    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    # Cleanup after test
    if os.path.exists(db_path):
        os.remove(db_path)
