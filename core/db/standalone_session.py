from uuid import uuid4

from .session import session, async_session, set_session_context, reset_session_context


def async_standalone_session(func):
    async def _async_standalone_session(*args, **kwargs):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await func(*args, **kwargs)
        except Exception as e:
            await async_session.rollback()
            raise e
        finally:
            await async_session.remove()
            reset_session_context(context=context)

    return _async_standalone_session


def standalone_session(func):
    print("standalone_session")

    """
        Useful for test case execution as the session context in the API is handled by middleware
    """
    def _standalone_session(*args, **kwargs):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        print("session_id", session_id)

        try:
            func(*args, **kwargs)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.remove()
            reset_session_context(context=context)

    return _standalone_session


class StandAloneSession:

    def __init__(self):
        self.session_id = str(uuid4())
        self.context = set_session_context(session_id=self.session_id)
        self.session = session


    def get_db_session(self):
        return self.session

    def wrap_session(self, func):
        print("standalone_session")

        """
            Useful for test case execution as the session context in the API is handled by middleware
        """
        def _standalone_session(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as e:

                raise e
            finally:

                reset_session_context(context=self.context)

        return _standalone_session


