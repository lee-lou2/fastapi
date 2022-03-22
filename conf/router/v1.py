from fastapi import APIRouter

from apps.backend.auth.user import views as user
from apps.backend.auth.account import views as account
from apps.backend.auth.token import views as token
from apps.backend.service.notice import views as notice
from apps.backend.service.scheduler import views as scheduler
from apps.backend.chatbot.memo import views as memo
from apps.backend.chatbot.alarm import views as alarm
from apps.backend.chatbot.question import views as question
from apps.backend.external.cafe24 import views as cafe24_product
from apps.backend.external.kakao import views as ka_ka_o_product
from apps.backend.websocket.chat import views as chat_web_socket
from apps.frontend.websocket.chat import views as front_chat_web_socket


api_v1_router = APIRouter()
api_v1_router.include_router(user.router_v1, prefix="/auth/user", tags=["user"])
api_v1_router.include_router(account.router_v1, prefix="/auth/account", tags=["account"])
api_v1_router.include_router(token.router_v1, prefix="/auth/token", tags=["token"])
api_v1_router.include_router(notice.router_v1, prefix="/notice", tags=["notice"])
api_v1_router.include_router(scheduler.router_v1, prefix="/scheduler", tags=["scheduler"])
api_v1_router.include_router(memo.router_v1, prefix="/chat_bot/memo", tags=["memo"])
api_v1_router.include_router(alarm.router_v1, prefix="/chat_bot/alarm", tags=["alarm"])
api_v1_router.include_router(question.router_v1, prefix="/chat_bot/question", tags=["question"])
api_v1_router.include_router(cafe24_product.router_v1, prefix="/external/cafe24", tags=["cafe24"])
api_v1_router.include_router(ka_ka_o_product.router_v1, prefix="/external/ka_ka_o", tags=["ka_ka_o"])
api_v1_router.include_router(front_chat_web_socket.router_v1, prefix="/web_socket/chat", tags=["front_chat_web_socket"])
api_v1_router.include_router(chat_web_socket.router_v1, prefix="/web_socket/chat", tags=["chat_web_socket"])

