from datetime import datetime, timedelta
from typing import Union

import jwt
from fastapi import HTTPException

from core import exceptions as ex
from conf.settings.prod import settings
from ..schemas import TokenGenerationIn, CodeType, DefaultTokenResponse, TokenGenerationOut, \
    TokenDecodeOut
from conf.caches import token_cache


class TokenManager:
    """
    토큰 관리
    """

    def __init__(
            self,
            token_data: TokenGenerationIn,
    ):
        self.token_data = token_data
        self.delta = None

    @staticmethod
    def _set_token_white_list(obj: dict):
        """
        화이트리스트 생성
        :param obj:
        :return:
        """
        # 사용자 정보로 토큰 조회
        token_cache.rpush(obj.get('user_id'), obj.get('token'))
        for _ in range(token_cache.llen(obj.get('user_id')) - 2):
            token_cache.delete(token_cache.lpop(obj.get('user_id')))
        # 신규 토큰 추가
        token_cache.set(obj.get('token'), '', obj.get('exp'))
        return True

    @staticmethod
    def _token_decode_valid(token: str):
        """
        화이트리스트 확인
        :param token:
        :return:
        """
        # 토큰 존재 여부 확인
        return token_cache.exists(token)

    def _token_generation(
            self,
            code_type: Union[str, CodeType]
    ) -> TokenGenerationOut:
        """
        토큰 생성
        :return:
        """
        if self.delta is None:
            raise ex.AuthExceptions.ExpiredToken
        # 토큰 유효 시간 지정
        delta = self.delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES
        # 딕셔너리로 변환
        to_encode = self.token_data.dict()
        # 유효 시간 설정
        to_encode.update({'code_type': code_type})
        to_encode.update({'iat': datetime.utcnow()})
        to_encode.update({'exp': datetime.utcnow() + timedelta(minutes=delta)})

        # 시크릿키 적용
        secret_key = \
            code_type == CodeType.A and settings.TOKEN_SECRET_KEY or settings.REFRESH_TOKEN_SECRET_KEY

        # 토큰 생성
        encoded_jwt = jwt.encode(
            to_encode,
            secret_key,
            algorithm=settings.ALGORITHM
        )
        # 화이트리스트 저장
        white_list_data = {
            'user_id': to_encode.get('user_id'),
            'token': encoded_jwt,
            'exp': timedelta(minutes=delta),
            'code_type': code_type
        }
        if not self._set_token_white_list(white_list_data):
            raise Exception('화이트리스트 생성 실패')
        res_token = {
            'token': encoded_jwt,
            'iat': to_encode.get('iat'),
            'exp': to_encode.get('exp')
        }
        return TokenGenerationOut(**res_token)

    def _get_token(
            self,
            code_type: Union[str, CodeType] = CodeType.A,
            delta: int = None
    ) -> TokenGenerationOut:
        """
        기본 토큰 생성
        :param code_type:
        :param delta:
        :return:
        """
        # 토큰 타입 확인
        if code_type == CodeType.R and delta is None:
            delta = settings.REFRESH_TOKEN_EXPIRE_MINUTES
        self.delta = delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES
        return self._token_generation(code_type)

    def get_default_token(self) -> DefaultTokenResponse:
        """
        액세스, 리프레시 토큰 일괄 생성
        :return:
        """
        tokens = {
            'access_token': self._get_token(CodeType.A),
            'refresh_token': self._get_token(CodeType.R)
        }
        return DefaultTokenResponse(**tokens)

    @staticmethod
    def decode_client_keys(
            key: str
    ) -> list:
        """
        클라이언트 키 해독
        :param key:
        :return:
        """
        import base64
        encode_key = key.encode('utf-8')
        bs64_decode = base64.b64decode(encode_key)
        decode_key = bs64_decode.decode('utf-8')
        return decode_key.split(':')

    @staticmethod
    def decode_token(
            token: str,
            code_type: Union[str, CodeType] = CodeType.A
    ) -> TokenDecodeOut:
        try:
            # 토큰 유효성 검사
            if not TokenManager._token_decode_valid(token):
                raise Exception('유효하지 않은 토큰입니다')

            # 시크릿키 적용
            secret_key = \
                code_type == CodeType.A and settings.TOKEN_SECRET_KEY or settings.REFRESH_TOKEN_SECRET_KEY

            # 토큰 복호화
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=[settings.ALGORITHM]
            )
            return TokenDecodeOut(**payload)
        except jwt.exceptions.ExpiredSignatureError as jwt_ex:
            # 토큰 유효기간 초과
            raise HTTPException(status_code=400, detail=str(jwt_ex))
        except jwt.exceptions.DecodeError as jwt_ex:
            # 유효하지 않은 토큰
            raise HTTPException(status_code=400, detail=str(jwt_ex))
        except jwt.exceptions.InvalidTokenError as jwt_ex:
            # 기타 오류
            raise HTTPException(status_code=400, detail=str(jwt_ex))
        except Exception as jwt_ex:
            # 최종 오류
            raise HTTPException(status_code=400, detail=str(jwt_ex))
