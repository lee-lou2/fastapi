from apps.backend.auth.user.schemas import UserPasswordRequest


class UserLoginRequest(UserPasswordRequest):
    email: str

    class Config:
        schema_extra = {
            "example": {
                "email": "admin@foo.com",
                "password": "<VERY_SAFE_PASSWORD>",
            }
        }
