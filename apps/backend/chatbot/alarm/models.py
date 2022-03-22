from sqlalchemy import Column, Integer, ForeignKey, DateTime, SmallInteger
from sqlalchemy.orm import relationship

from conf.databases import TimeStamp, DefaultBase


class ChatBotAlarm(DefaultBase, TimeStamp):
    # 시간 설정
    next_alarm = Column(DateTime, nullable=True)
    time_interval = Column(SmallInteger, default=0)
    last_alarm = Column(DateTime, nullable=True)
    # 연결된 챗봇
    chat_bot_content_id = Column(Integer, ForeignKey('chat_bot_content.id'))

    chat_bot_content = relationship('ChatBotContent', back_populates='chat_bot_alarm')
