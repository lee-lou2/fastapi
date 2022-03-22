from fastapi import APIRouter, Depends
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session
from starlette.requests import Request

from core import exceptions as ex
from core.authorization import ClientKeyAuthorization
from conf.databases import get_db
from conf.throttling import limiter
from .schemas import TokenGenerationIn, DefaultTokenResponse, RefreshTokenRequest, TokenRequestRequest, CodeType
from .controllers.manager import TokenManager
from ..user.models import User, UserSecret

# 라우터
router_v1 = APIRouter()
# 리미터
limiter = limiter.init


@router_v1.post('/', response_model=DefaultTokenResponse, dependencies=[Depends(ClientKeyAuthorization())])
@limiter.limit("1/second")
def get_token(
        request: Request,
        *,
        db: Session = Depends(get_db),
        obj_in: TokenRequestRequest,
) -> DefaultTokenResponse:
    """
    토큰 생성\n
    [필수] headers = {'Authorization': 'Basic [client_id:client_secret(base64 encoding)]'}
    \n\n
    :param request:
    :param db:
    :param obj_in:
    :return:
    """
    # 인증 정보 수집
    authorization: str = request.headers.get("Authorization")
    scheme, credentials = get_authorization_scheme_param(authorization)
    # 유효성 검사
    if not authorization or scheme.lower() != "basic":
        raise ex.AuthExceptions.NotFoundClientKeys
    if obj_in.grant_type != 'authorization_code':
        raise ex.AuthExceptions.NotFoundClientKeys

    # 클라이언트 키 해독
    client_keys = TokenManager.decode_client_keys(credentials)

    # 키 변수 지정
    client_id = client_keys[0] if len(client_keys) > 1 else None
    client_secret = client_keys[1] if len(client_keys) > 1 else None

    # 데이터 조회
    user = db.query(UserSecret).filter_by(
        client_id=client_id,
        client_secret=client_secret
    ).first()
    if not user:
        raise ex.AuthExceptions.NotFoundUser
    return TokenManager(TokenGenerationIn(user_id=user.user_id)).get_default_token()


@router_v1.post('/refresh', response_model=DefaultTokenResponse)
def refresh_token(
        *,
        db: Session = Depends(get_db),
        obj_in: RefreshTokenRequest,
) -> DefaultTokenResponse:
    """
    토큰 재발급
    :param db:
    :param obj_in:
    :return:
    """
    decode_token = TokenManager.decode_token(token=obj_in.refresh_token, code_type=CodeType.R)

    user = db.query(User).get(decode_token.user_id)
    if not user:
        raise ex.AuthExceptions.NotFoundUser
    token_data = {'user_id': user.id}
    return TokenManager(TokenGenerationIn(**token_data)).get_default_token()
