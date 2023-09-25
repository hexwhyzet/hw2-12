from sqlalchemy import Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from dal.base import Base
from dal.user import User


class Post(Base):
    __tablename__ = 'post'

    BACK_POPULATES = 'posts'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    text = mapped_column("text", VARCHAR(256), nullable=False)
    user_id = mapped_column("user_id", Integer, ForeignKey(User.id), nullable=False)

    user = relationship(User, foreign_keys=user_id, backref=BACK_POPULATES)
