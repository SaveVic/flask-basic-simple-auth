from random import randint
from flask.testing import FlaskClient
from tests.conftest import AuthActions
from flaskr.util.random import get_random_user


def test_access_api_unauthorized(client: FlaskClient):
    with client:
        response = client.get('/api', follow_redirects=True)
        assert response.status_code == 404
        assert response.request.path == '/api'
        assert b'Something wrong!' in response.data


def test_access_api_authorized(client: FlaskClient, auth: AuthActions):
    count = randint(1, 5)
    users = []
    with client:
        for _ in range(count):
            username, email, password = get_random_user().to_dict().values()
            auth.register(client, username, password, email)
            users.append((username, password))
            auth.logout(client)

    with client:
        idx = randint(0, count-1)
        auth.login(client, users[idx][0], users[idx][1])
        response = client.get('/api', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/api'
        assert f'User Count : {count}'.encode() in response.data
        assert users[idx][0].encode() in response.data
