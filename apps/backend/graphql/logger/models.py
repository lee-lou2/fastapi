from sqlalchemy import Column, String

from conf.databases import LogBase, TimeStamp


class Log(LogBase, TimeStamp):
    """
    로그 기록
    """
    url = Column(String)
    log_level = Column(String)
    message = Column(String)
