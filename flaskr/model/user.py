from typing import Union
from flaskr.model.schema import User


class UserModel:
    def __init__(
        self,
        id: Union[int, None] = None,
        username: Union[str, None] = None,
        email: Union[str, None] = None,
        password: Union[str, None] = None,
    ) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def factory(cls, user: User):
        return UserModel(user.id, user.username, user.email, user.password)

    def to_dict(self, exclude_id=True):
        d = {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        if not exclude_id:
            d['id'] = self.id
        return d

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, username={self.username!r}, password={self.password!r} email={self.email!r})'  # pragma: no cover
