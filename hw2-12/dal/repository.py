from os import environ
from typing import Type, List

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class BaseRepository:
    def add(self, entity: DeclarativeBase):
        raise NotImplementedError

    def remove(self, entity: DeclarativeBase):
        raise NotImplementedError

    def get_by_id(self, table: Type, id: int) -> DeclarativeBase:
        raise NotImplementedError

    def list(self, table: Type) -> List[Type]:
        raise NotImplementedError

    def update(self, entity: DeclarativeBase):
        raise NotImplementedError

    def filter_by(self, entity: DeclarativeBase):
        raise NotImplementedError


class SQLAlchemyRepository(BaseRepository):
    def __init__(self, session: Session):
        self.__session = session

    def add(self, entity: DeclarativeBase):
        try:
            self.__session.add(entity)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def remove(self, entity: DeclarativeBase):
        self.__session.delete(entity)
        try:
            self.__session.add(entity)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def get_by_id(self, table: Type, id: int):
        return self.__session.get(table, id)

    def list(self, table: Type) -> List[Type]:
        return self.__session.query(table).all()

    def update(self, entity: DeclarativeBase):
        fields_to_update = {}
        for column in entity.__table__.columns.keys():
            if column not in ["id"]:
                fields_to_update[column] = entity.__dict__[column]
        entity_type = type(entity)
        self.__session.query(entity_type).filter(entity_type.id == entity.id).update(fields_to_update)
        try:
            self.__session.add(entity)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def filter_by(self, table: Type, **kwargs):
        return self.__session.query(table).filter_by(**kwargs)


def get_sessionmaker():
    engine = create_engine(
        f"postgresql://{environ.get('DB_USER')}:{environ.get('DB_PASSWORD')}@{environ.get('DB_HOST')}:{environ.get('DB_PORT')}/{environ.get('DB_DATABASE')}"
    )
    return sessionmaker(engine, autocommit=False, autoflush=True)


def get_repository(sessionmaker):
    session = sessionmaker()
    repository = SQLAlchemyRepository(session)
    try:
        yield repository
    finally:
        session.close()
