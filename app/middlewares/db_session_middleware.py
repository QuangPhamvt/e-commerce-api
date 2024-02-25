from fastapi import Request, Response
from app.database import SessionLocal


async def db_session_middleware(request: Request, call_next):
    """
    Middleware to manage the database session
    request: Request object from FastAPI
    call_next: function to call the next middleware
    """
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
