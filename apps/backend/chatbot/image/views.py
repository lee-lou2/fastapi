from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from conf.databases import get_db

# 라우터
router_v1 = APIRouter()


def add_content(body: bytes, db: Session):
    from core.choices import ChatBotContentTypeChoices
    from apps.backend.chatbot.base.controllers.properties import KaKaoProperty
    prop = KaKaoProperty(body, db, ChatBotContentTypeChoices.IMG.name)
    prop.save()
    return prop


@router_v1.post("/", status_code=201)
async def create_image(
        *,
        request: Request,
        db: Session = Depends(get_db)
):
    body = await request.body()
    content = add_content(body, db)

    from core.consts import DEFAULT_KA_KA_O_RESPONSE_TEMPLATE
    response = DEFAULT_KA_KA_O_RESPONSE_TEMPLATE
    response['template']['outputs'][0]['listCard']['items'][0]['title'] = '이미지가 등록되었습니다.' \
        if content.is_created else '이미지 등록이 중단되었습니다.'
    response['template']['outputs'][0]['listCard']['items'][0]['description'] = ': ' + content.content
    return response
