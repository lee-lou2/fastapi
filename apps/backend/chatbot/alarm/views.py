from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from conf.databases import get_db
from apps.backend.chatbot.alarm.models import *

# 라우터
router_v1 = APIRouter()


def add_content(body: bytes, db: Session):
    from core.choices import ChatBotContentTypeChoices
    from apps.backend.chatbot.base.controllers.properties import KaKaoProperty
    prop = KaKaoProperty(body, db, ChatBotContentTypeChoices.A.name)
    prop.save()
    return prop


def run_delete_alarm(body, db):
    from core.choices import ChatBotContentTypeChoices
    from apps.backend.chatbot.base.controllers.properties import KaKaoProperty
    prop = KaKaoProperty(body, db, ChatBotContentTypeChoices.DA.name)
    prop.delete()


@router_v1.post("/", status_code=201)
async def create_alarm(
        *,
        request: Request,
        db: Session = Depends(get_db)
):
    body = await request.body()
    content = add_content(body, db)

    from core.consts import DEFAULT_KA_KA_O_RESPONSE_TEMPLATE
    response = DEFAULT_KA_KA_O_RESPONSE_TEMPLATE
    response['template']['outputs'][0]['listCard']['items'][0]['title'] = '알림이 생성되었습니다.' \
        if content.is_created else '알람 생성이 중단되었습니다.'
    response['template']['outputs'][0]['listCard']['items'][0]['description'] = ': ' + content.content
    return response


@router_v1.post("/delete", status_code=201)
async def delete_alarm(
        *,
        request: Request,
        db: Session = Depends(get_db)
):
    body = await request.body()
    run_delete_alarm(body, db)

    from core.consts import DEFAULT_KA_KA_O_RESPONSE_TEMPLATE
    response = DEFAULT_KA_KA_O_RESPONSE_TEMPLATE
    response['template']['outputs'][0]['listCard']['items'][0]['title'] = '알림이 삭제되었습니다.'
    response['template']['outputs'][0]['listCard']['items'][0]['description'] = ''
    return response
