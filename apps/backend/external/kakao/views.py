from fastapi import APIRouter, Request
from starlette.background import BackgroundTasks

from apps.backend.external.kakao.controllers.message import send_to_you_message, MessageTemplate
from apps.backend.external.kakao.schemas import SendToMeDefaultMessageRequestBase

# 라우터
router_v1 = APIRouter()


@router_v1.post("/", status_code=201)
async def send_to_me_text_message(
        *,
        request: Request,
        background_tasks: BackgroundTasks,
        obj_in: SendToMeDefaultMessageRequestBase
):
    from conf.caches import ka_ka_o_cache
    access_token = ka_ka_o_cache.get('access_token')
    template = MessageTemplate.default_text(obj_in.message)
    background_tasks.add_task(
        send_to_you_message,
        access_token=access_token,
        template=template
    )
    return None
