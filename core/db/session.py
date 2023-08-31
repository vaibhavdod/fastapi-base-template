import logging
from typing import Generator
from threading import get_ident
from contextvars import ContextVar, Token
from typing import Union

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.sql.expression import Update, Delete, Insert

from core.config import config

log = logging.getLogger(__name__)

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)



def create_async_session(async_db=True):
    
    if async_db and config.ASYNC_WRITER_DB_URI and config.ASYNC_READER_DB_URI:
        async_engines = {
            "writer": create_async_engine(config.ASYNC_WRITER_DB_URI, pool_recycle=config.DB_ENGINE_POOL_SIZE),
            "reader": create_async_engine(config.ASYNC_READER_DB_URI, pool_recycle=config.DB_ENGINE_POOL_SIZE),
        }


        class AsyncRoutingSession(Session):
            def get_bind(self, mapper=None, clause=None, **kw):
                if self._flushing or isinstance(clause, (Update, Delete, Insert)):
                    return async_engines["writer"].sync_engine
                else:
                    return async_engines["reader"].sync_engine

        async_session_factory = sessionmaker(
            class_=AsyncSession,
            sync_session_class=AsyncRoutingSession,
        )

        async_session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
            session_factory=async_session_factory,
            scopefunc=get_session_context,
        )

        return async_session

    elif async_db and (config.ASYNC_WRITER_DB_URI is None or config.ASYNC_READER_DB_URI is None):
        log.warning("Invalid Configurations: Async DB URI not provided")


def create_session():

    # Sync DB session creation

    engines = {
        "writer": create_engine(config.WRITER_DB_URI, pool_size=config.DB_ENGINE_POOL_SIZE, max_overflow=config.DB_ENGINE_MAX_OVERFLOW),
        "reader": create_engine(config.READER_DB_URI, pool_size=config.DB_ENGINE_POOL_SIZE, max_overflow=config.DB_ENGINE_MAX_OVERFLOW),
    }

    class RoutingSession(Session):
        def get_bind(self, mapper=None, clause=None, **kw):
            if self._flushing or isinstance(clause, (Update, Delete, Insert)):
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
    database_sesssion : Union[Session, scoped_session] = scoped_session(session_factory, scopefunc=get_session_context)

    # this is to handle standaone session, where we don't have any middleware to handle session context
    # TODO: can be handled in a better way but engine dinging is not working for database_sesssion
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engines["writer"])
    
    return database_sesssion, SessionLocal


session, SessionLocal = create_session()


async_session = create_async_session(async_db=False) 

Base = declarative_base()