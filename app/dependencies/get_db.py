from fastapi import Request


def get_db(request: Request):
    """
    This is a simple function that takes a request and returns the database session.
    request: Request - The request object.
    """
    return request.state.db
