from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.http import HTTPBase

from apps.backend.auth.token.schemas import CodeType
from apps.backend.auth.token.controllers.manager import TokenManager


class BearerBase(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(BearerBase, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme."
                )
            TokenManager.decode_token(token=credentials.credentials, code_type=self.code_type)
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid authorization code."
            )


class BearerAccessToken(BearerBase):
    def __init__(self, auto_error: bool = True):
        self.code_type = CodeType.A
        super(BearerBase, self).__init__(auto_error=auto_error, scheme_name='Access Token')


class BearerRefreshToken(BearerBase):
    def __init__(self, auto_error: bool = True):
        self.code_type = CodeType.R
        super(BearerBase, self).__init__(auto_error=auto_error, scheme_name='Refresh Token')


class ClientKeyAuthorization(HTTPBase):
    def __init__(self):
        super(ClientKeyAuthorization, self).__init__(
            scheme='basic',
            auto_error=True,
            scheme_name='Client Key'
        )
