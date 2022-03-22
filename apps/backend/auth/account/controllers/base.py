from abc import abstractmethod, ABCMeta

from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from starlette.requests import Request

from conf.settings.prod import settings

# Oauth 생성
from core.choices import SocialTypeChoices

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.SOCIAL_ACCOUNT_GOOGLE_CLIENT_ID,
    client_secret=settings.SOCIAL_ACCOUNT_GOOGLE_SECRET,
    server_metadata_url=settings.SOCIAL_ACCOUNT_GOOGLE_CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


class SocialBase:
    def __init__(self, social_type: str = SocialTypeChoices.G.value):
        self.social_type = social_type
        self.oauth = oauth.create_client(self.social_type)


class SocialLogin(SocialBase):
    @property
    def get_redirect_uri(self):
        """
        리다이렉트 주소 조회
        """
        if self.social_type == SocialTypeChoices.G.value:
            return '/v1/auth/account/google/login/callback'

    def authorize_redirect(self, request: Request):
        """
        리다이렉트
        """
        client_host = request.headers.get('host')
        redirect_uri = f'http://{client_host}{self.get_redirect_uri}'
        return self.oauth.authorize_redirect(request, redirect_uri)


class SocialCallBack(SocialBase):
    @property
    def get_call_back_class(self):
        """
        콜백 클래스 조회
        """
        social_class = None
        if self.social_type == SocialTypeChoices.G.value:
            from apps.backend.auth.account.controllers.google import SocialCallBackGoogle
            social_class = SocialCallBackGoogle
        return social_class


class SocialCallBackBase(SocialBase, metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validated_data = None
        self.model = None
        self.db = None

    @abstractmethod
    def is_valid(self, user: dict):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def get_or_create_user(self, request: Request, db: Session):
        pass
