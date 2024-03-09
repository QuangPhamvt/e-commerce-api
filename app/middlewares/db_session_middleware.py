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
        print("Opening database session")
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        await request.state.db.close()
        print("Closing database session")
    return response
