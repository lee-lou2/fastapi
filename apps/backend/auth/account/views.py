import json

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

# 라우터
from apps.backend.auth.account.schemas import UserLoginRequest
from apps.backend.auth.token.schemas import DefaultTokenResponse, TokenGenerationIn
from conf.databases import get_db

router_v1 = APIRouter()


@router_v1.get('/')
async def homepage(
        request: Request
):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = f'<pre>{data}</pre><a href="/v1/auth/account/logout">logout</a>'
        return HTMLResponse(html)
    return HTMLResponse('<a href="/v1/auth/account/google/login">google login</a>')


@router_v1.post('/login', response_model=DefaultTokenResponse, status_code=201)
async def local_login(
        obj_in: UserLoginRequest,
        db: Session = Depends(get_db),
) -> DefaultTokenResponse:
    from core import exceptions as ex
    from core.security import verify_password
    from apps.backend.auth.user.models import User
    from apps.backend.auth.token.controllers.manager import TokenManager

    # 데이터 조회
    user_data = obj_in.dict()
    user = db.query(User).filter_by(
        email=user_data.get('email')
    ).first()
    # 로컬 유저가 있는지 확인
    if user is None or user.user_local is None:
        raise ex.AuthExceptions.NotFoundLocalUser
    # 해시 패스워드 조회
    if not verify_password(user_data.get('password'), user.user_local.password):
        raise ex.AuthExceptions.PasswordValidationError
    return TokenManager(TokenGenerationIn(user_id=user.id)).get_default_token()


@router_v1.get('/{social_type}/login')
async def social_login(request: Request, social_type: str):
    from apps.backend.auth.account.controllers.base import SocialLogin
    return await SocialLogin(social_type=social_type).authorize_redirect(request)


@router_v1.get('/{social_type}/login/callback', response_model=DefaultTokenResponse)
async def social_callback(
        request: Request,
        social_type: str,
        db: Session = Depends(get_db),
) -> DefaultTokenResponse:
    from apps.backend.auth.token.controllers.manager import TokenManager
    from apps.backend.auth.account.controllers.base import SocialCallBack

    # 타입별 콜백 클래스 조회
    call_back = SocialCallBack(social_type=social_type).get_call_back_class()
    # 해당 클래스의 사용자 조회
    user = await call_back.get_or_create_user(request, db)
    # 사용자 확인시 토큰 발급
    return TokenManager(TokenGenerationIn(user_id=user.id)).get_default_token()


@router_v1.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/v1/auth/account/')
