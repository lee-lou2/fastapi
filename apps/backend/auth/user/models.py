import uuid as uuid

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from apps.backend.auth.account.models import UserSocial, UserLocal
from conf.databases import TimeStamp, DefaultBase


class UserSecret(DefaultBase):
    """
    사용자 인증 정보
    """
    # 클라이언트 아이디
    client_id = Column(String, nullable=False)
    # 클라이언트 시크릿
    client_secret = Column(String, nullable=False)
    # 연결된 사용자
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='user_secret')


class User(DefaultBase, TimeStamp):
    """
    사용자 기본
    """
    # UUID
    uuid = Column(UUIDType, unique=True, default=uuid.uuid4)
    # 이메일 주소
    email = Column(String, unique=True, nullable=False)
    # 삭제 여부
    is_deleted = Column(Boolean, default=False)
    # 관리자 여부
    is_admin = Column(Boolean, default=False)

    user_secret = relationship('UserSecret', back_populates='user', uselist=False)
    user_social = relationship(UserSocial, back_populates='user')
    user_local = relationship(UserLocal, back_populates='user', uselist=False)
    security_rsa_key_set = relationship('SecurityRSAKeySet', back_populates='user', uselist=False)

    @classmethod
    def merge_or_create_user(cls, db, data: dict):
        """
        로컬 사용자 생성
        이미 동일한 이메일이 있는 경우 통합
        """
        user = db.query(cls).filter_by(email=data.get('email')).first()
        if user is None:
            user = cls(
                email=data.get('email')
            )
            db.add(user)
        user_local = UserLocal(
            user=user,
            password=data.get('password')
        )
        client_keys = UserSecret(
            user=user,
            client_id=data.get('client_id'),
            client_secret=data.get('client_secret')
        )
        db.add(user_local)
        db.add(client_keys)
        db.commit()
