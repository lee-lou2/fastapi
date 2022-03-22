from fastapi import Request, Response

from conf.databases import DefaultSession


async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = DefaultSession()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
