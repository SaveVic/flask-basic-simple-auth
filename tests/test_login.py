from flask import session, g
from flask.testing import FlaskClient
import pytest
from flaskr.repo.user import get_one
from tests.conftest import AuthActions
from flaskr.util.random import get_random_user


@pytest.mark.parametrize(
    argnames=('username', 'password', 'message'),
    argvalues=(
        ('', '', b'Username is required!'),
        ('tname', '', b'Password is required!'),
    ),
)
def test_login_invalid(client: FlaskClient, auth: AuthActions, username, password, message):
    with client:
        response = auth.login(client, username, password)
        assert response.status_code == 200
        assert response.request.path == '/login'
        assert message in response.data
        # session
        assert 'id' not in session
    with client:
        client.get('/')
        assert 'user' not in g


def test_login_success(client: FlaskClient, auth: AuthActions):
    username, email, password = get_random_user().to_dict().values()
    with client:
        auth.register(client, username, password, email)
        auth.logout(client)
        response = auth.login(client, username, password)
        assert response.status_code == 200
        assert response.request.path == '/'
        assert f'Hello, {username}'.encode() in response.data
        # session
        user = get_one(username=username, email=email)
        assert session.get('id', None) == user.id
    with client:
        client.get('/')
        assert g.get('user', None) is not None


def test_login_incorrect_username(client: FlaskClient, auth: AuthActions):
    username, email, password = get_random_user().to_dict().values()
    rand_user = get_random_user()
    with client:
        auth.register(client, username, password, email)
        auth.logout(client)
        response = auth.login(client, rand_user.username, password)
        assert response.status_code == 200
        assert response.request.path == '/login'
        assert b'Incorrect username / password!' in response.data
        # session
        assert 'id' not in session
    with client:
        client.get('/')
        assert 'user' not in g


def test_login_incorrect_password(client: FlaskClient, auth: AuthActions):
    username, email, password = get_random_user().to_dict().values()
    rand_user = get_random_user()
    with client:
        auth.register(client, username, password, email)
        auth.logout(client)
        response = auth.login(client, username, rand_user.password)
        assert response.status_code == 200
        assert response.request.path == '/login'
        assert b'Incorrect username / password!' in response.data
        # session
        assert 'id' not in session
    with client:
        client.get('/')
        assert 'user' not in g


def test_login_while_logged_in(client: FlaskClient, auth: AuthActions):
    user1 = get_random_user()
    user2 = get_random_user()
    with client:
        auth.register(client, user1.username, user1.password, user1.email)
        auth.logout(client)
        auth.register(client, user2.username, user2.password, user2.email)
        response = auth.login(client, user1.username, user1.password)
        assert response.status_code == 200
        assert response.request.path == '/'
        assert f'Hello, {user2.username}'.encode() in response.data
        # session
        assert 'id' in session
        assert g.get('user', None) is not None


def test_login_page(client: FlaskClient):
    with client:
        response = client.get('/login')
        assert response.status_code == 200
        assert response.request.path == '/login'
        assert b'Login' in response.data
        # session
        assert 'id' not in session
        assert g.get('user', None) is None


def test_login_page_while_logged_in(client: FlaskClient, auth: AuthActions):
    username, email, password = get_random_user().to_dict().values()
    with client:
        auth.register(client, username, password, email)
        response = client.get('/login', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/'
        assert f'Hello, {username}'.encode() in response.data
        # session
        assert 'id' in session
        assert g.get('user', None) is not None
