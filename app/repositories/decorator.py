import functools

from sqlalchemy.exc import SQLAlchemyError

from app.core.errors import ServiceUnavailableError

def handle_db_errors(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except SQLAlchemyError:
            raise ServiceUnavailableError(meta={"source": "db"})
        except Exception as e:
            raise e
    return wrapper