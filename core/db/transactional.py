from functools import wraps

from core.db import session, async_session


class AsyncTransactional:
    def __call__(self, func):
        @wraps(func)
        async def _transactional(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                await async_session.commit()
            except Exception as e:
                await async_session.rollback()
                raise e

            return result

        return _transactional
    

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