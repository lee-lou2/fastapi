from typing import List

from pydantic import BaseModel


class BaseNotice(BaseModel):
    message: str


class SendEmailIn(BaseModel):
    email: str


class SendEmailListRequest(BaseNotice):
    subject: str
    users: List[SendEmailIn]

    class Config:
        schema_extra = {
            "example": {
                "message": "이메일 내용",
                "subject": "이메일 제목",
                "users": [
                    {
                        "email": "admin@foo.com"
                    },
                    {
                        "email": "user@foo.com"
                    }
                ]
            }
        }


class SendEmailInIamRequest(BaseNotice):
    subject: str
    email: str
    name: str

    class Config:
        schema_extra = {
            "example": {
                "email": "admin@foo.com",
                "name": "<NAME>",
                "subject": "이메일 제목",
                "message": "이메일 내용",
            }
        }


class SendSMSRequest(BaseNotice):
    phone: str

    class Config:
        schema_extra = {
            "example": {
                "message": "문자 내용",
                "phone": "010-0000-0000",
            }
        }


class SendSlackRequest(BaseNotice):
    room: str

    class Config:
        schema_extra = {
            "example": {
                "message": "슬랙 내용",
                "room": "slack_room",
            }
        }

