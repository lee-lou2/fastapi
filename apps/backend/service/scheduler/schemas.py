from enum import Enum


class ScheduleName(str, Enum):
    CAFE24_REFRESH_TOKEN: str = 'cafe24_refresh_token'
    KAKAO_REFRESH_TOKEN: str = 'kakao_refresh_token'
    SEND_STOCK: str = 'send_stock'
    ALARM_SERVICE: str = 'alarm_service'
    CRAWLING: str = 'crawling'
    ETC: str = 'etc'
