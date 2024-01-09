from flask import current_app
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from typing import TypeVar, Callable, Union
from flaskr.model.schema import init_db


T = TypeVar('T')


__engine: Union[Engine, None] = None


def _get_engine():
    global __engine
    if __engine is None:
        path = current_app.config['DATABASE']
        __engine = create_engine(f'sqlite:///{path}', echo=True)
        init_db(__engine)
    return __engine


def execute(func: Callable[[Session], T]) -> T:
    with Session(_get_engine()) as db_sess:
        result = func(db_sess)
        return result


def dispose():
    global __engine
    if __engine is not None:
        __engine.dispose()
        __engine = None
