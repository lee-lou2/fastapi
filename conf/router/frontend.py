from fastapi import APIRouter

from apps.frontend.websocket.chat import views as front_chat_web_socket
from apps.frontend.chatbot.memo import views as front_chat_bot_memo


frontend_router = APIRouter()

frontend_router.include_router(front_chat_web_socket.router_v1, prefix="/web_socket/chat", tags=["front_chat_web_socket"])
frontend_router.include_router(front_chat_bot_memo.router_v1, prefix="/chat_bot/memo", tags=["front_chat_web_socket"])
