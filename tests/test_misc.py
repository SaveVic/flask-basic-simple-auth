from flask import session, g
from flask.testing import FlaskClient
from tests.conftest import AuthActions
from flaskr.util.random import get_random_user


def test_invalid_id_in_session(client: FlaskClient, auth: AuthActions):
    username, email, password = get_random_user().to_dict().values()
    with client:
        auth.register(client, username, password, email)
        with client.session_transaction() as sess:
            sess['id'] = 999
        client.get('/')
        assert 'id' not in session
        assert 'user' not in g
