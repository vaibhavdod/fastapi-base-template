import logging
from contextvars import ContextVar, Token
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.sql.expression import Delete, Insert, Update

from core.config import config

log = logging.getLogger(__name__)

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


def create_session():
    # Sync DB session creation

    engines = {
        "writer": create_engine(
            config.WRITER_DB_URI,
            pool_size=config.DB_ENGINE_POOL_SIZE,
            max_overflow=config.DB_ENGINE_MAX_OVERFLOW,
        ),
        "reader": create_engine(
            config.READER_DB_URI,
            pool_size=config.DB_ENGINE_POOL_SIZE,
            max_overflow=config.DB_ENGINE_MAX_OVERFLOW,
        ),
    }

    class RoutingSession(Session):
        def get_bind(self, mapper=None, clause=None, **kw):
            if self._flushing or isinstance(clause, (Update, Delete, Insert)):  # type: ignore
                return engines["writer"]
            else:
                return engines["reader"]

    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        class_=Session,
        session_factory=RoutingSession,
    )

    # Scoped session helps in the web based API hits so that every time each request has it's own fresh session context
    database_sesssion: Union[Session, scoped_session] = scoped_session(
        session_factory, scopefunc=get_session_context
    )

    # this is to handle standaone session, where we don't have any middleware to handle session context
    # TODO: can be handled in a better way but engine dinging is not working for database_sesssion
    SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engines["writer"]
    )

    return database_sesssion, SessionLocal


session, SessionLocal = create_session()


Base = declarative_base()
