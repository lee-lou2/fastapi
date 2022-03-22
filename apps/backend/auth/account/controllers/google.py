from authlib.integrations.base_client import OAuthError
from sqlalchemy.orm import Session
from starlette.requests import Request

from apps.backend.auth.account.controllers.base import SocialCallBackBase


class SocialCallBackGoogle(SocialCallBackBase):
    def get_user_or_none(self, email: str):
        assert self.db, '데이터베이스 설정이 정상적으로 되지 않았습니다.'

        from apps.backend.auth.user.models import User
        user = self.db.query(User).filter_by(email=email).first()
        return user

    def is_valid(self, user: dict):
        """
        유효성 검사
        """
        # 변수 지정
        sub = user.get('sub')
        email = user.get('email')
        name = user.get('name')
        picture = user.get('picture')
        # 유효성 검사
        if not email or str(email) == '':
            raise
        # 데이터 저장
        self.validated_data = {
            'sub': sub,
            'email': email,
            'name': name,
            'picture': picture
        }

    def save(self):
        """
        저장
        """
        assert self.db, '데이터베이스 설정이 정상적으로 되지 않았습니다.'
        assert self.validated_data, '유효성 검사 후에 사용 가능합니다.'

        import secrets
        from core.choices import SocialTypeChoices
        from apps.backend.auth.user.models import User, UserSecret
        from apps.backend.auth.account.models import UserSocial, UserProfile

        client_id = secrets.token_hex(32)
        client_secret = secrets.token_hex(32)
        user = User(
            email=self.validated_data.get('email'),
        )
        client_keys = UserSecret(
            user=user,
            client_id=client_id,
            client_secret=client_secret
        )
        social = UserSocial(
            social_id=self.validated_data.get('sub'),
            social_type=SocialTypeChoices.G.name,
            user=user
        )
        social_profile = UserProfile(
            user_social=social,
            name=self.validated_data.get('name'),
            picture=self.validated_data.get('picture'),
        )
        self.db.add(user)
        self.db.add(social)
        self.db.add(social_profile)
        self.db.add(client_keys)
        self.db.commit()
        return user

    async def get_or_create_user(self, request: Request, db: Session):
        try:
            token = await self.oauth.authorize_access_token(request)
        except OAuthError as err:
            from core import exceptions as ex
            raise ex.AuthExceptions.SocialLoginError
        # 데이터베이스 설정
        self.db = db
        # 소셜 정보 조회
        social_user = await self.oauth.userinfo(token=token)
        email = dict(social_user).get('email')
        user = self.get_user_or_none(email)
        if user is None:
            self.is_valid(social_user)
            user = self.save()
        return user
