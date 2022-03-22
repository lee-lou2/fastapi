from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserPasswordRequest(BaseModel):
    password: str

    class Config:
        schema_extra = {
            "example": {
                "password": "<VERY_SAFE_PASSWORD>"
            }
        }


class UserListResponse(BaseModel):
    created: Optional[datetime]
    email: str

    class Config:
        schema_extra = {
            "example": {
                "created": "2021-01-01 00:00:0000",
                "email": "admin@foo.com",
            }
        }


class UserPasswordCreateRequest(BaseModel):
    password1: str
    password2: str

    class Config:
        schema_extra = {
            "example": {
                "password1": "<VERY_SAFE_PASSWORD1>",
                "password2": "<VERY_SAFE_PASSWORD2>"
            }
        }


class UserCreateRequest(UserPasswordCreateRequest):
    email: str

    class Config:
        schema_extra = {
            "example": {
                "email": "admin@foo.com",
                "password1": "<VERY_SAFE_PASSWORD1>",
                "password2": "<VERY_SAFE_PASSWORD2>",
            }
        }


class UserCreateResponse(BaseModel):
    email: str
    client_id: str
    client_secret: str

    class Config:
        schema_extra = {
            "example": {
                "email": "admin@foo.com",
                "client_id": "<CLIENT_ID>",
                "client_secret": "<CLIENT_SECRET>",
            }
        }


class GetCurrentUserResponse(BaseModel):
    email: str
    is_active: bool
    is_superuser: bool
