import redis

from conf.settings.prod import settings


# 변수 선언
CACHE_URL = settings.CACHE_URL if not settings.TEST_MODE else settings.TEST_CACHE_URL
CACHE_PORT = settings.CACHE_PORT if not settings.TEST_MODE else settings.TEST_CACHE_PORT

# 캐시
token_cache = redis.StrictRedis(
    host=CACHE_URL,
    port=CACHE_PORT,
    db=1,
    decode_responses=True
)
cafe24_cache = redis.StrictRedis(
    host=CACHE_URL,
    port=CACHE_PORT,
    db=2,
    decode_responses=True
)
ka_ka_o_cache = redis.StrictRedis(
    host=CACHE_URL,
    port=CACHE_PORT,
    db=3,
    decode_responses=True
)
memo_cache = redis.StrictRedis(
    host=CACHE_URL,
    port=CACHE_PORT,
    db=4,
    decode_responses=True
)

# 리미터 URL
limiter_cache_url = f"redis://{CACHE_URL}:{CACHE_PORT}/0"
