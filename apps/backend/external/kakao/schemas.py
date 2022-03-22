from pydantic import BaseModel


class SendToMeDefaultMessageRequestBase(BaseModel):
    message: str
