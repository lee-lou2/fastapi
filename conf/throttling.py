from slowapi import Limiter
from slowapi.util import get_remote_address

from conf.caches import limiter_cache_url


class BaseLimiter:
    """
    리미터 생성
    """
    def __init__(self):
        self.key_func = get_remote_address
        self.storage_uri = limiter_cache_url

    @property
    def init(self):
        return Limiter(
            key_func=self.key_func,
            storage_uri=self.storage_uri,
            default_limits=["1/second"],
        )


limiter = BaseLimiter()
