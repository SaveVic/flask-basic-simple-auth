from flask import session, g
from flaskr.model.user import UserModel
import flaskr.repo.user as repo

__keys = ['id']


def set_session(data: UserModel) -> None:
    session.clear()
    data_dict = data.to_dict(exclude_id=False)
    for k in __keys:
        session[k] = data_dict.get(k, None)


def is_logged_in() -> bool:
    return g.get('user', None) is not None


def load_from_session() -> None:
    id = session.get('id')
    if id is None:
        return
    user = repo.get_one(id=id)
    if user is None:
        clear_session()
        return
    g.user = user


def clear_session() -> None:
    session.clear()
