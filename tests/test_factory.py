from flask.testing import FlaskClient
from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client: FlaskClient):
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'


def test_index(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Simple Auth' in response.data
