from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from conf.databases import get_db
from conf.router.deps import get_current_user
from core import exceptions as ex
from core.authorization import BearerAccessToken
from core.security import get_password_hash
from .controllers.validation import get_by_email
from .models import (
    User,
    UserSecret,
)
from .schemas import (
    UserPasswordRequest,
    UserCreateRequest,
    UserCreateResponse
)

# 라우터
from ..account.models import UserLocal

router_v1 = APIRouter()


@router_v1.post("/sign_up", response_model=UserCreateResponse, status_code=201)
async def create_user(
        *,
        db: Session = Depends(get_db),
        obj_in: UserCreateRequest,
) -> UserCreateResponse:
    """
    유저 생성
    :param db:
    :param obj_in:
    :return:
    """
    import secrets

    insert_data = obj_in.dict()

    # 이메일주소 중복 확인
    if get_by_email(db, insert_data.get('email')):
        raise ex.AuthExceptions.ExistEmail

    # 패스워드 암호화
    password1 = insert_data.pop('password1')
    password2 = insert_data.pop('password2')
    if password1 != password2:
        raise ex.AuthExceptions.PasswordValidationError
    insert_data['password'] = get_password_hash(password1)

    # 클라이언트 키 적용
    client_id = secrets.token_hex(32)
    client_secret = secrets.token_hex(32)
    insert_data['client_id'] = client_id
    insert_data['client_secret'] = client_secret
    if db.query(UserSecret).filter_by(
            client_id=client_id,
            client_secret=client_secret
    ).count() > 0:
        raise ex.AuthExceptions.ExistClientKeys

    # 데이터베이스 저장
    User.merge_or_create_user(db, insert_data)

    return UserCreateResponse(
        email=insert_data.get('email'),
        client_id=insert_data.get('client_id'),
        client_secret=insert_data.get('client_secret')
    )


@router_v1.patch("/", status_code=204, dependencies=[Depends(BearerAccessToken())])
async def change_password(
        *,
        db: Session = Depends(get_db),
        obj_in: UserPasswordRequest,
        current_user: User = Depends(get_current_user)
) -> None:
    """
    패스워드 변경
    :param db:
    :param obj_in:
    :param current_user:
    :return:
    """
    if current_user is None:
        raise ex.AuthExceptions.NotFoundUser
    if current_user.user_local is None:
        raise ex.AuthExceptions.NotFoundLocalUser
    current_user.user_local.password = get_password_hash(obj_in.password)
    db.commit()
    return None
