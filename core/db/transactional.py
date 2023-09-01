from functools import wraps

from core.db import session


class Transactional:
    def __call__(self, func):
        @wraps(func)
        def _transactional(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

            return result

        return _transactional
