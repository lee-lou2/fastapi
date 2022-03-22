import logging

from fastapi import FastAPI, Request
from fastapi.logger import logger
from fastapi.staticfiles import StaticFiles

from slowapi import _rate_limit_exceeded_handler as rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.testclient import TestClient

from apps.backend.graphql.logger.views import graphql_app
from conf.settings.prod import settings
from conf.databases import DefaultBase, default_engine, log_engine, LogBase
from core.middlewares.database import db_session_middleware
from core.middlewares.trusted_hosts import TrustedHostMiddleware
from conf.throttling import limiter
from conf.router.v1 import api_v1_router

# -------
# 기본 설정
# -------
from core.utils.logger import DatabaseHandler

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)

# ----
# 테스트
# ----
test_client = TestClient(app)

# ----------
# Throttling
# ----------
limiter = limiter.init
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


# ------
# Logger
# ------
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s'))
logger.addHandler(ch)
sqlite_handler = DatabaseHandler()
logger.addHandler(sqlite_handler)

# ------------
# 데이터베이스 생성
# ------------
DefaultBase.metadata.create_all(bind=default_engine)
LogBase.metadata.create_all(bind=log_engine)

# ---------
# 미들웨어 정의
# ---------
# 데이터베이스 세션 생성
app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=db_session_middleware
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.TRUSTED_HOSTS,
    except_path=["/health"]
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)


@app.middleware("http")
async def add_default_middleware(request: Request, call_next):
    import time
    from core.utils.logger import api_logger
    from conf.router.deps import get_user_id
    request.state.start = time.time()
    # 사용자 조회
    request.state.user = await get_user_id(request=request)
    # IP 조회
    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    start_time = time.time()
    # API 호출
    response = await call_next(request)
    # 로그 기록
    await api_logger(request=request, response=response)
    # API 구동 시간 기록
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# -----------
# Static File
# -----------
app.mount("/static", StaticFiles(directory=f"{settings.BASE_PATH}/static"), name="static")

# --------
# 라우터 정의
# --------
app.include_router(
    api_v1_router,
    prefix=settings.API_V1_STR
)
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


# -----------------
# Application Event
# -----------------
@app.on_event("startup")
async def startup_event():
    print('Hello!')


@app.on_event("shutdown")
def shutdown_event():
    print('Bye~')
