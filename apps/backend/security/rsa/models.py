import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from conf.databases import DefaultBase


class SecurityRSAKeySet(DefaultBase):
    """
    RSA 키셋
    """
    # 공개키
    public_key = Column(String, nullable=False)
    # 비밀키
    private_key = Column(String, nullable=False)
    # 만료일
    expire_at = Column(
        DateTime,
        default=datetime.datetime.utcnow()
    )
    # 연결된 사용자
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)

    user = relationship('User', back_populates='security_rsa_key_set')

    def decrypt_data(self, public_key, encrypted_base64_data):
        import base64
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_OAEP

        key = self.validate_public_key(public_key).first()
        private_key = RSA.importKey(key.private_key)
        encrypted_data = base64.b64decode(encrypted_base64_data)
        decrypter = PKCS1_OAEP.new(private_key)
        decrypted = decrypter.decrypt(encrypted_data)
        return decrypted.decode()

    def create_key_set(self, user = None):
        from Crypto import Random
        from Crypto.PublicKey import RSA

        key_pair = RSA.generate(1024, Random.new().read)
        public_key = key_pair.publickey().exportKey().decode('ascii')
        private_key = key_pair.exportKey().decode('ascii')
        expire_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)

        return SecurityRSAKeySet(
            public_key=public_key,
            private_key=private_key,
            expire_at=expire_at,
            user=user
        )
