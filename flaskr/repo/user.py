from typing import Union
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from flaskr.model.user import UserModel
from flaskr.model.schema import User
from flaskr.util.db import execute


def get_all() -> list[UserModel]:
    stmt = select(User)

    def func(db_sess: Session):
        result = db_sess.scalars(stmt).all()
        users = [UserModel.factory(user) for user in result]
        return users

    return execute(func)


def get_one(
        id: Union[int, None] = None,
        username: Union[str, None] = None,
        email: Union[str, None] = None,
        username_or_email: Union[tuple[str, str], None] = None
) -> Union[UserModel, None]:
    stmt = select(User)
    if id is not None:
        stmt = stmt.filter(User.id == id)
    if username_or_email is not None:
        u, e = username_or_email
        stmt = stmt.filter(or_(User.username == u, User.email == e))
    if username is not None:
        stmt = stmt.filter(User.username == username)
    if email is not None:
        stmt = stmt.filter(User.email == email)

    def func(db_sess: Session):
        result = db_sess.scalars(stmt).one_or_none()
        return None if result is None else UserModel.factory(result)

    return execute(func)


def insert(data: UserModel):
    user = get_one(username_or_email=(data.username, data.email))
    if user is not None:
        return None

    def func(db_sess: Session):
        new_user = User(**data.to_dict())
        db_sess.add(new_user)
        db_sess.commit()
        return UserModel.factory(new_user)

    return execute(func)
