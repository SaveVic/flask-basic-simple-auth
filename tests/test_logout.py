from flask import session, g
from flask.testing import FlaskClient
from tests.conftest import AuthActions
from flaskr.util.random import get_random_user


def test_logout(client: FlaskClient, auth: AuthActions):
    with client:
        response = auth.logout(client)
        assert response.status_code == 200
        assert response.request.path == '/'
        assert b'Simple Auth' in response.data
        # session
        assert 'id' not in session
    with client:
        client.get('/')
        assert 'user' not in g


def test_logout_after_register(client: FlaskClient, auth: AuthActions):
    username, email, password = get_random_user().to_dict().values()
    with client:
        auth.register(client, username, password, email)
        response = auth.logout(client)
        assert response.status_code == 200
        assert response.request.path == '/'
        assert b'Simple Auth' in response.data
        # session
        assert 'id' not in session
    with client:
        client.get('/')
        assert 'user' not in g


def test_logout_after_login(client: FlaskClient, auth: AuthActions):
    username, email, password = get_random_user().to_dict().values()
    with client:
        auth.register(client, username, password, email)
        auth.logout(client)
        auth.login(client, username, password)
        response = auth.logout(client)
        assert response.status_code == 200
        assert response.request.path == '/'
        assert b'Simple Auth' in response.data
        # session
        assert 'id' not in session
    with client:
        client.get('/')
        assert 'user' not in g
