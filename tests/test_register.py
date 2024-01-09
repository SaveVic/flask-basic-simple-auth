from flask import session, g
from flask.testing import FlaskClient
import pytest
from flaskr.repo.user import get_one
from tests.conftest import AuthActions
from flaskr.util.random import get_random_user


@pytest.mark.parametrize(
    argnames=('username', 'password', 'email', 'message'),
    argvalues=(
        ('', '', '', b'Username is required!'),
        ('tname-', '', '', b'Username must contain only characters and numbers!'),
        ('tname', '', '', b'Password is required!'),
        ('tname', 'tpass', '', b'Email is required!'),
        ('tname', 'tpass', 'tmail', b'Invalid email address!'),
        ('tname', 'tpass', 'tmail@', b'Invalid email address!'),
        ('tname', 'tpass', 'tmail@tmail', b'Invalid email address!'),
        ('tname', 'tpass', '@tmail', b'Invalid email address!'),
    ),
)
def test_register_invalid(client: FlaskClient, auth: AuthActions, username, password, email, message):
    with client:
        response = auth.register(client, username, password, email)
        assert response.status_code == 200
        assert response.request.path == '/register'
        assert message in response.data
        # session
        assert 'id' not in session
    with client:
        client.get('/')
        assert 'user' not in g


def test_register_success(client: FlaskClient, auth: AuthActions):
    username, email, password = get_random_user().to_dict().values()
    with client:
        response = auth.register(client, username, password, email)
        assert response.status_code == 200
        assert response.request.path == '/'
        assert f'Hello, {username}'.encode() in response.data
        # db
        user = get_one(username=username, email=email)
        assert user is not None
        # session
        assert session.get('id', None) == user.id
    with client:
        client.get('/')
        assert g.get('user', None) is not None


def test_register_same_username(client: FlaskClient, auth: AuthActions):
    username, email, password = get_random_user().to_dict().values()
    rand_user = get_random_user()
    with client:
        auth.register(client, username, password, email)
        auth.logout(client)
        response = auth.register(
            client, username, rand_user.password, rand_user.email)
        assert response.status_code == 200
        assert response.request.path == '/register'
        assert b'Account already exists!' in response.data
        # session
        assert 'id' not in session
    with client:
        client.get('/')
        assert 'user' not in g


def test_register_same_email(client: FlaskClient, auth: AuthActions):
    username, email, password = get_random_user().to_dict().values()
    rand_user = get_random_user()
    with client:
        auth.register(client, username, password, email)
        auth.logout(client)
        response = auth.register(
            client, rand_user.username, rand_user.password, email)
        assert response.status_code == 200
        assert response.request.path == '/register'
        assert b'Account already exists!' in response.data
        # session
        assert 'id' not in session
    with client:
        client.get('/')
        assert 'user' not in g


def test_register_while_logged_in(client: FlaskClient, auth: AuthActions):
    user1 = get_random_user()
    user2 = get_random_user()
    with client:
        auth.register(client, user1.username, user1.password, user1.email)
        response = auth.register(
            client, user2.username, user2.password, user2.email)
        assert response.status_code == 200
        assert response.request.path == '/'
        assert f'Hello, {user1.username}'.encode() in response.data
        # session
        assert 'id' in session
        assert g.get('user', None) is not None


def test_register_page(client: FlaskClient):
    with client:
        response = client.get('/register')
        assert response.status_code == 200
        assert response.request.path == '/register'
        assert b'Register' in response.data
        # session
        assert 'id' not in session
        assert g.get('user', None) is None


def test_register_page_while_logged_in(client: FlaskClient, auth: AuthActions):
    username, email, password = get_random_user().to_dict().values()
    with client:
        auth.register(client, username, password, email)
        response = client.get('/register', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/'
        assert f'Hello, {username}'.encode() in response.data
        # session
        assert 'id' in session
        assert g.get('user', None) is not None
