import flaskr.repo.user as repo
from flaskr.model.user import UserModel
from flaskr.util.validator import Validator
from werkzeug.security import check_password_hash, generate_password_hash


def login(data: dict[str, str]):
    msg = Validator(data).set_field('username').is_not_empty().set_field(
        'password').is_not_empty().msg()
    if msg is not None:
        return msg
    user_data = UserModel(**data)
    user = repo.get_one(username=user_data.username)
    if user is None or not check_password_hash(user.password, user_data.password):
        return 'Incorrect username / password!'
    return user


def register(data: dict[str, str]):
    msg = Validator(data).set_field('username').is_not_empty().is_alphanumeric().set_field(
        'password').is_not_empty().set_field('email').is_not_empty().is_email().msg()
    if msg is not None:
        return msg
    user_data = UserModel(**data)
    user_data.password = generate_password_hash(user_data.password)
    user = repo.insert(user_data)
    if user is None:
        return 'Account already exists!'
    return user
