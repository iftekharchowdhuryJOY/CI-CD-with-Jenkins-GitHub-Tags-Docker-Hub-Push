from app.main import app

def test_home():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b"Hello from Jenkins CI/CD!" in response.data

