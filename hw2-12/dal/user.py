from sqlalchemy import Integer, VARCHAR, Table, Column, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from dal.base import Base


class User(Base):
    __tablename__ = 'user'

    BACK_POPULATES = 'users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column("name", VARCHAR(256), nullable=False)

    following = relationship(
        'User', lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        backref='followers'
    )


user_following = Table(
    'user_following', Base.metadata,
    Column('user_id', Integer, ForeignKey(User.id), primary_key=True),
    Column('following_id', Integer, ForeignKey(User.id), primary_key=True)
)
