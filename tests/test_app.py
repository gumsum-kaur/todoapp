
import pytest
from todo_app.app import app
from todo_app.database import init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()  # Reset schema before each test
        yield client

def test_get_tasks(client):
    # Request JSON response from the UI route
    resp = client.get('/app/tasks', headers={'Accept': 'application/json'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)

def test_create_task(client):
    payload = {
        'title': 'Test Task',
        'description': 'Test Desc',
        'due_date': '2025-12-27',
        'status': 'pending'
    }
    resp = client.post('/api/tasks', json=payload)
    assert resp.status_code == 201
    out = resp.get_json()
    assert 'id' in out

def test_get_task(client):
    # Create first
    client.post('/api/tasks', json={'title': 'Test Task'})
    resp = client.get('/api/tasks/1')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['title'] == 'Test Task'

def test_update_task(client):
    # Create
    client.post('/api/tasks', json={'title': 'Old Title'})
    # Update
    resp = client.put('/api/tasks/1', json={'title': 'New Title'})
    assert resp.status_code == 200
    # Verify
    updated = client.get('/api/tasks/1')
    assert updated.status_code == 200
    assert updated.get_json()['title'] == 'New Title'

def test_delete_task(client):
    client.post('/api/tasks', json={'title': 'To Delete'})
    resp = client.delete('/api/tasks/1')
    assert resp.status_code == 200
    # Delete
    assert client.get('/api/tasks/1').status_code == 404
