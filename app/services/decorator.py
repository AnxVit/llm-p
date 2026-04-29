import functools
from httpx import HTTPStatusError

from app.core.errors import ServiceUnavailableError

def handle_service_errors(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except HTTPStatusError as e:
            if e.response.status_code == 503:
                raise ServiceUnavailableError(meta={"source": "openrouter"})
            raise e
    return wrapper