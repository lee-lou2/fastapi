from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, Enum, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from conf.databases import DefaultBase
from conf.settings.prod import settings
from core.choices import SocialTypeChoices


class UserLocal(DefaultBase):
    """
    자체 가입자
    """
    # 패스워드
    password = Column(String, nullable=False)
    # 사용 여부
    is_active = Column(Boolean, default=True)
    # 연결된 사용자
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='user_local')
    user_profile = relationship(
        'UserProfile',
        back_populates='user_local',
        uselist=False
    )


class UserSocial(DefaultBase):
    """
    소셜 가입자
    """
    # 소셜 아이디
    social_id = Column(String, unique=True, nullable=False)
    # 소셜 타입
    social_type = Column(
        Enum(SocialTypeChoices),
        nullable=False,
        default=SocialTypeChoices.G.name
    )
    # 사용 여부
    is_active = Column(Boolean, default=True)
    # 연결된 사용자
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='user_social')
    user_profile = relationship(
        'UserProfile',
        back_populates='user_social',
        uselist=False
    )


class UserProfile(DefaultBase):
    """
    소셜 가입자 프로필
    """
    # 이름
    name = Column(EncryptedType(
        Unicode, settings.DATABASE_ENCRYPT_KEY, AesEngine, "pkcs5"
    ))
    # 사진
    picture = Column(EncryptedType(
        Unicode, settings.DATABASE_ENCRYPT_KEY, AesEngine, "pkcs5"
    ))
    # 연결된 소셜 사용자
    user_social_id = Column(Integer, ForeignKey('user_social.id'))
    # 연결된 자체 사용자
    user_local_id = Column(Integer, ForeignKey('user_local.id'))

    user_social = relationship(UserSocial, back_populates='user_profile')
    user_local = relationship(UserLocal, back_populates='user_profile')
