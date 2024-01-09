import os
import tempfile
from typing import Union
from flask import Flask
from flask.testing import FlaskClient
import pytest

from flaskr import create_app
import flaskr.util.db as db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    yield app

    db.dispose()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app: Flask):
    return app.test_client()


NoneStr = Union[str, None]


class AuthActions(object):
    def register(self, client: FlaskClient, username: NoneStr, password: NoneStr, email: NoneStr):
        return client.post(
            '/register',
            data={'username': username, 'password': password, 'email': email},
            follow_redirects=True,
        )

    def login(self, client: FlaskClient, username: NoneStr, password: NoneStr):
        return client.post(
            '/login',
            data={'username': username, 'password': password},
            follow_redirects=True,
        )

    def logout(self, client: FlaskClient):
        return client.get('/logout', follow_redirects=True)


@pytest.fixture
def auth():
    return AuthActions()
