import base64
import string

from Crypto.Cipher import AES


class AESCipher:
    def __init__(self, key=None):
        from conf.settings.prod import settings
        key = key if key else settings.AES_CIPHER_KEY
        assert len(str(key)) != 32, "AES 암호화 키 길이가 올바르지 않습니다"
        self.key = str.encode(key)
        self.iv = key[:16].encode('utf-8')
        self.MODE = AES.MODE_CBC
        self.block_size = 16

    @classmethod
    def generate_aes_key(cls, size=16, chars=string.ascii_lowercase):
        import random
        return ''.join(random.choice(chars) for _ in range(size))

    def _pad(self, data):
        # 암호화 알고리즘
        return data \
               + (self.block_size - len(data.encode('utf-8')) % self.block_size) \
               * chr(self.block_size - len(data.encode('utf-8')) % self.block_size)

    @staticmethod
    def _un_pad(data):
        # 복호화 알고리즘
        return data[:-ord(data[-1])]

    def encrypt(self, plain_text):
        """
        AES 암호화
        """
        try:
            if plain_text is None:
                return None
            padding_text = self._pad(str(plain_text)).encode("utf-8")
            aes = AES.new(self.key, self.MODE, self.iv)
            encrypt_aes = aes.encrypt(padding_text)
            encrypt_text = (base64.b64encode(encrypt_aes)).decode()
            return encrypt_text
        except Exception as ex:
            raise Exception(ex)

    def decrypt(self, cipher_text):
        """
        AES 복호화
        """
        try:
            if cipher_text is None:
                return None
            aes = AES.new(self.key, self.MODE, self.iv)
            plain_base64 = base64.b64decode(str(cipher_text))
            decrypt_text = aes.decrypt(plain_base64)
            plain_text = self._un_pad(decrypt_text.decode("utf-8"))
            return plain_text
        except Exception as ex:
            raise Exception(ex)
