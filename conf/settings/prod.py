from os import path, environ

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env', verbose=True)


# 기본 디렉토리
base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


class BaseConfig:
    """
    기본 설정
    """
    # 테스트 모드
    TEST_MODE: bool = bool(environ.get('TEST_MODE', False))
    # 프로젝트 이름
    PROJECT_NAME: str = environ.get('PROJECT_NAME')
    PROJECT_DESCRIPTION: str = environ.get('PROJECT_DESCRIPTION')
    PROJECT_VERSION: str = environ.get('PROJECT_VERSION')
    # 허용할 CORS
    BACKEND_CORS_ORIGINS: list = [
        origin.strip()
        for origin in str(environ.get('BACKEND_CORS_ORIGINS', '')).split(',')
        if origin is not None and origin.strip() != ''
    ]
    # 접근 가능한 호스트
    TRUSTED_HOSTS: list = [
        host.strip()
        for host in str(environ.get('TRUSTED_HOSTS', '')).split(',')
        if host is not None and host.strip() != ''
    ]
    # 프로젝트 시크릿키
    SECRET_KEY: str = environ.get('SECRET_KEY')
    # Static Path
    BASE_PATH: str = environ.get('BASE_PATH', '.')


class Token:
    # 토큰 허용 기간
    TOKEN_SECRET_KEY = environ.get('TOKEN_SECRET_KEY')
    REFRESH_TOKEN_SECRET_KEY = environ.get('REFRESH_TOKEN_SECRET_KEY')
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 2
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7


class Notice:
    EMAIL_ADDRESS = environ.get("EMAIL_ADDRESS")
    EMAIL_PASSWORD = environ.get("EMAIL_PASSWORD")
    RECEIVE_EMAIL_ADDRESS = environ.get("RECEIVE_EMAIL_ADDRESS")
    NAVER_CLOUD_SID = environ.get("NAVER_CLOUD_SID")
    NAVER_CLOUD_ACCESS_KEY_ID = environ.get("NAVER_CLOUD_ACCESS_KEY_ID")
    NAVER_CLOUD_ACCESS_SECRET_KEY = environ.get(
        "NAVER_CLOUD_ACCESS_SECRET_KEY"
    ).encode('ascii')
    SMS_FROM_NO = environ.get("SMS_FROM_NO")
    SLACK_KEY = environ.get("SLACK_KEY")


class Version:
    # API V1
    API_V1_STR: str = "/v1"


class Database:
    # 데이터베이스 URL
    MONGODB_URL: str = environ.get('MONGODB_URL')
    # 데이터베이스 URL
    SQLITE_URL: str = environ.get('SQLITE_URL')
    POSTGRESQL_URL: str = environ.get('POSTGRESQL_URL')
    TEST_DATABASE_URL: str = environ.get('TEST_DATABASE_URL')
    # 리사이클 시간
    SQLITE_POOL_RECYCLE: int = int(environ.get('SQLITE_POOL_RECYCLE', 900))
    # 애코 여부
    SQLITE_ECHO: bool = bool(environ.get('SQLITE_ECHO', False))
    # 엘라스틱서치 주소
    ELASTICSEARCH_URL: str = environ.get('ELASTICSEARCH_URL')
    ELASTICSEARCH_PORT: str = environ.get('ELASTICSEARCH_PORT')
    ELASTICSEARCH_USERNAME: str = environ.get('ELASTICSEARCH_USERNAME')
    ELASTICSEARCH_PASSWORD: str = environ.get('ELASTICSEARCH_PASSWORD')
    LOGS_SQLITE_URL: str = environ.get('LOGS_SQLITE_URL')
    JOBS_SQLITE_URL: str = environ.get('JOBS_SQLITE_URL')


class Cache:
    # 캐시 URL
    CACHE_URL: str = environ.get('CACHE_URL')
    CACHE_PORT: int = environ.get('CACHE_PORT', 6379)
    TEST_CACHE_URL: str = environ.get('TEST_CACHE_URL')
    TEST_CACHE_PORT: int = environ.get('TEST_CACHE_PORT', 6379)
    CELERY_BROKER_URL: str = f"redis://{CACHE_URL}:{CACHE_PORT}/0"
    CELERY_RESULT_BACKEND: str = f"redis://{CACHE_URL}:{CACHE_PORT}/0"


class SocialLogin:
    # Google
    SOCIAL_ACCOUNT_GOOGLE_CLIENT_ID = environ.get('SOCIAL_ACCOUNT_GOOGLE_CLIENT_ID')
    SOCIAL_ACCOUNT_GOOGLE_SECRET = environ.get('SOCIAL_ACCOUNT_GOOGLE_SECRET')
    SOCIAL_ACCOUNT_GOOGLE_CONF_URL = environ.get('SOCIAL_ACCOUNT_GOOGLE_CONF_URL')
    # Apple
    SOCIAL_ACCOUNT_APPLE_CLIENT_ID = environ.get('SOCIAL_ACCOUNT_APPLE_CLIENT_ID')
    SOCIAL_ACCOUNT_APPLE_SECRET = environ.get('SOCIAL_ACCOUNT_APPLE_SECRET')
    # Naver
    SOCIAL_ACCOUNT_NAVER_CLIENT_ID = environ.get('SOCIAL_ACCOUNT_NAVER_CLIENT_ID')
    SOCIAL_ACCOUNT_NAVER_SECRET = environ.get('SOCIAL_ACCOUNT_NAVER_SECRET')
    # Kakao
    SOCIAL_ACCOUNT_KAKAO_CLIENT_ID = environ.get('SOCIAL_ACCOUNT_KAKAO_CLIENT_ID')


class Encrypt:
    # 암호화 키
    DATABASE_ENCRYPT_KEY = environ.get('DATABASE_ENCRYPT_KEY')
    AES_CIPHER_KEY = environ.get('AES_CIPHER_KEY')


class ExternalService:
    CAFE24_MARKET_B_TOKEN_URL = environ.get('CAFE24_MARKET_B_TOKEN_URL')
    CAFE24_MARKET_B_MALL_ID = environ.get('CAFE24_MARKET_B_MALL_ID')
    CAFE24_LOU_2_MALL_ID = environ.get('CAFE24_LOU_2_MALL_ID')
    CAFE24_LOU_2_CLIENT_ID = environ.get('CAFE24_LOU_2_CLIENT_ID')
    CAFE24_LOU_2_CLIENT_SECRET = environ.get('CAFE24_LOU_2_CLIENT_SECRET')
    CAFE24_LOU_2_REDIRECT_URL = environ.get('CAFE24_LOU_2_REDIRECT_URL')
    CAFE24_LOU_2_MASTER_ID = environ.get('CAFE24_LOU_2_MASTER_ID')
    CAFE24_LOU_2_MASTER_PASSWORD = environ.get('CAFE24_LOU_2_MASTER_PASSWORD')
    CAFE24_LOU_2_DEFAULT_REFRESH_TOKEN = environ.get('CAFE24_LOU_2_DEFAULT_REFRESH_TOKEN')
    CAFE24_LOU_2_DEFAULT_VERSION = environ.get('CAFE24_LOU_2_DEFAULT_VERSION')

    # 카카오
    KAKAO_SEND_MESSAGE_CLIENT_ID = environ.get('KAKAO_SEND_MESSAGE_CLIENT_ID')
    KAKAO_MESSAGE_DEFAULT_REFRESH_TOKEN = environ.get('KAKAO_MESSAGE_DEFAULT_REFRESH_TOKEN')
    KAKAO_SEND_MESSAGE_REDIRECT_URL = environ.get('KAKAO_SEND_MESSAGE_REDIRECT_URL')
    KAKAO_SEND_MESSAGE_CODE = environ.get('KAKAO_SEND_MESSAGE_CODE')
    KAKAO_SEND_MESSAGE_SCOPE = environ.get('KAKAO_SEND_MESSAGE_SCOPE')
    KAKAO_MY_UUID = environ.get('KAKAO_MY_UUID')

    SEND_STOCK_MY_CODE = environ.get('SEND_STOCK_MY_CODE')
    SEND_STOCK_BUY_PRICE = environ.get('SEND_STOCK_BUY_PRICE')
    SEND_STOCK_QTY = environ.get('SEND_STOCK_QTY')


class FTPAccount:
    FTP_CONNECT_URL = environ.get('FTP_CONNECT_URL')
    FTP_CONNECT_ID = environ.get('FTP_CONNECT_ID')
    FTP_CONNECT_PASSWORD = environ.get('FTP_CONNECT_PASSWORD')
    FTP_CONNECT_UPLOAD_PATH = environ.get('FTP_CONNECT_UPLOAD_PATH')


class Settings(BaseSettings,
               BaseConfig,
               Token,
               Version,
               Database,
               Cache,
               Notice,
               SocialLogin,
               Encrypt,
               ExternalService,
               FTPAccount):

    class Config:
        case_sensitive = True


settings = Settings()
