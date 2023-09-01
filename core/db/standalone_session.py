from uuid import uuid4

from .session import reset_session_context, session, set_session_context


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
