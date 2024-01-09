from sqlalchemy import Engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class __Base(DeclarativeBase):
    pass


class User(__Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, username={self.username!r}, email={self.email!r})'  # pragma: no cover


def init_db(engine: Engine):
    __Base.metadata.create_all(engine)
