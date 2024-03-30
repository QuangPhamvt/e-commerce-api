import logging
import time
from fastapi import Request


async def log_middleware(request: Request, call_next):
    """
    Middleware to log the request and response of the server and the process time
    request: Request object from FastAPI
    call_next: function to call the next middleware
    """
    log = logging.getLogger("uvicorn")
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    log.info(f"Process time: {process_time}")
    return response
