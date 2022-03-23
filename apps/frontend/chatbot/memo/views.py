from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from conf.databases import get_db
from core.templates import template

router_v1 = APIRouter()


@router_v1.get("/")
async def memo(
        *,
        request: Request,
        friend_key: str = None,
        db: Session = Depends(get_db)
):
    from conf.caches import memo_cache
    from apps.backend.chatbot.base.models import ChatBot, ChatBotContent

    # 캐시에 저장되어있는지 확인
    if memo_cache.exists(friend_key):
        chat_bot = db.query(ChatBot).filter_by(friend_key=friend_key).first()
        contents = db.query(ChatBotContent).filter_by(chat_bot=chat_bot)
        memo_list = [(content.content, content.id) for content in contents]
    else:
        from core import exceptions as ex
        raise ex.FrontendExceptions.ExpiredFriend
    return template.init.TemplateResponse(
        "chatbot/memo.html",
        {
            "request": request,
            "memo_list": memo_list
        }
    )
