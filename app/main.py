import uvicorn
import logging
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from core.config import config
from core.logging import configure_logging
from core.rate_limiter import limiter


configure_logging(config.LOG_LEVEL)

log = logging.getLogger(__name__)


async def not_found(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": [{"msg": "Not Found."}]}
    )
exception_handlers = {404: not_found}





def create_app():
    _app = FastAPI(exception_handlers=exception_handlers, openapi_url="")

    # Rate limiter middleware
    _app.state.limiter = limiter
    _app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    @_app.get("/check/")
    def check():
        return {"message": "Hello World"}


    log.debug("URS App created!-")
    return _app


app = create_app()