from fastapi import status
from fastapi.exceptions import HTTPException


class DatabaseExceptions:
    NotFoundObject = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='객체를 찾을 수 없습니다',
        headers={'code': '000001'}
    )


class AuthExceptions:
    NotFoundToken = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Not Found Token',
        headers={'code': '100001'}
    )

    NotFoundUser = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Not Found User',
        headers={'code': '100002'}
    )

    NotSuperUser = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Not Super User',
        headers={'code': '100003'}
    )

    ExpiredToken = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='Expired Token',
        headers={'code': '100004'}
    )

    NotFoundClientKeys = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Not Found Client Keys',
        headers={'code': '100005'}
    )

    ExistClientKeys = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='Exist Client Keys',
        headers={'code': '100006'}
    )

    ExistEmail = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='Exist Email',
        headers={'code': '100007'}
    )

    NotFoundLocation = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Not Found Location Name',
        headers={'code': '100008'}
    )

    SocialLoginError = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Social Login Error',
        headers={'code': '100009'}
    )

    NotFoundLocalUser = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='소셜 가입자는 패스워드 변경이 불가합니다',
        headers={'code': '100010'}
    )

    PasswordValidationError = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='패스워드가 일치하지 않습니다',
        headers={'code': '100011'}
    )


class ProductExceptions:
    NotFoundDataBaseConnect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='데이터베이스 연결 데이터가 조회되지 않습니다',
        headers={'code': '110001'}
    )
    NotFoundProduct = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='제품이 생성되지 않았습니다',
        headers={'code': '110002'}
    )
    NotFoundBrandObject = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='브랜드가 존재하지 않습니다',
        headers={'code': '110003'}
    )


class CategoryExceptions:
    NotFoundObject = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='객체를 찾지 못했습니다',
        headers={'code': '120001'}
    )


class FrontendExceptions:
    ExpiredFriend = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='만료된 사용자 정보입니다',
        headers={'code': '130001'}
    )
