from enum import Enum
import datetime
from typing import Optional, List

from pydantic import BaseModel


class CodeType(str, Enum):
    A: str = 'access_token'
    R: str = 'refresh_token'


class TokenScope(str, Enum):
    send_sms: str = 'send_sms'
    send_email: str = 'send_email'


class TokenDecodeOut(BaseModel):
    user_id: str
    scopes: Optional[List[TokenScope]]


class TokenGenerationIn(TokenDecodeOut):
    delta: Optional[int]


class TokenGenerationOut(BaseModel):
    token: str
    type: Optional[str] = 'Bearer'
    iat: datetime.datetime
    exp: datetime.datetime


class DefaultTokenResponse(BaseModel):
    access_token: TokenGenerationOut
    refresh_token: TokenGenerationOut

    class Config:
        schema_extra = {
            "example": {
                "access_token": {
                    "token": "<ACCESS_TOKEN>",
                    "type": "Bearer",
                    "iat": "2021-01-01T01:00:00.000000",
                    "exp": "2021-01-01T02:00:00.000000"
                },
                "refresh_token": {
                    "token": "<REFRESH_TOKEN>",
                    "type": "Bearer",
                    "iat": "2021-01-01T01:00:00.000000",
                    "exp": "2021-01-02T01:00:00.000000"
                }
            }
        }


class RefreshTokenRequest(BaseModel):
    refresh_token: str

    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "<REFRESH_TOKEN>",
            }
        }


class TokenWhiteListCreateIn(BaseModel):
    user_id: int
    code_type: str
    token: Optional[str]
    exp: datetime.datetime


class TokenRequestRequest(BaseModel):
    grant_type: str = 'authorization_code'
    code: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "grant_type": "authorization_code",
                "code": "<AUTHORIZATION_CODE>",
            }
        }
