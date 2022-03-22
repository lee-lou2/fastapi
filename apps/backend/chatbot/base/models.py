from sqlalchemy import Column, Integer, String, ForeignKey, Unicode, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from conf.databases import TimeStamp, DefaultBase
from conf.settings.prod import settings
from core.choices import ChatBotContentTypeChoices


class ChatBot(DefaultBase):
    # 친구 키
    friend_key = Column(String, unique=True, nullable=False)

    chat_bot_content = relationship('ChatBotContent', back_populates='chat_bot')


class ChatBotContent(DefaultBase, TimeStamp):
    # 컨텐츠
    content = Column(EncryptedType(
        Unicode, settings.DATABASE_ENCRYPT_KEY, AesEngine, "pkcs5"
    ))
    # 블록 종류
    block_type = Column(
        Enum(ChatBotContentTypeChoices),
        nullable=False,
        default=ChatBotContentTypeChoices.T.name
    )
    # 연결된 챗봇
    chat_bot_id = Column(Integer, ForeignKey('chat_bot.id'))
    chat_bot_alarm = relationship('ChatBotAlarm', back_populates='chat_bot_content')

    chat_bot = relationship('ChatBot', back_populates='chat_bot_content')
