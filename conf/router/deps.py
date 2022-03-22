from fastapi import Depends
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session
from starlette.requests import Request

from apps.backend.auth.token.controllers.manager import TokenManager
from apps.backend.auth.user.models import User
from apps.backend.auth.token.schemas import TokenDecodeOut
from core import exceptions as ex
from conf.databases import get_db


async def get_token(
    request: Request,
) -> TokenDecodeOut:
    # 인증 정보 수집
    authorization: str = request.headers.get("Authorization")
    scheme, credentials = get_authorization_scheme_param(authorization)
    # 유효성 검사
    if not authorization or scheme.lower() != "bearer":
        raise ex.AuthExceptions.NotFoundToken
    # 디코드 토큰
    token = TokenManager.decode_token(credentials)
    return token


async def get_user_id(
        request: Request,
):
    # 인증 정보 수집
    authorization: str = request.headers.get("Authorization")
    scheme, credentials = get_authorization_scheme_param(authorization)
    # 유효성 검사
    if not authorization or scheme.lower() != "bearer":
        return None
    # 디코드 토큰
    token = TokenManager.decode_token(credentials)
    return token.user_id


async def get_current_user(
        token: TokenDecodeOut = Depends(get_token),
        db: Session = Depends(get_db),
) -> User:
    user = db.query(User).get(token.user_id)
    if not user:
        raise ex.AuthExceptions.NotFoundUser
    return user


async def get_current_superuser(
        current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise ex.AuthExceptions.NotSuperUser
    return current_user
