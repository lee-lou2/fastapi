import requests


class Token:
    def __init__(self):
        from conf.settings.prod import settings
        self.client_id = settings.KAKAO_SEND_MESSAGE_CLIENT_ID
        self.redirect_url = settings.KAKAO_SEND_MESSAGE_REDIRECT_URL
        self.code = settings.KAKAO_SEND_MESSAGE_CODE
        self.scope = settings.KAKAO_SEND_MESSAGE_SCOPE

    def create_tokens(self):
        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_url,
            "code": self.code
        }
        res = requests.post(url, data=data)

        if res.status_code == 200:
            from conf.caches import ka_ka_o_cache
            ka_ka_o_cache.set('access_token', res.json().get('access_token'))
            ka_ka_o_cache.set('refresh_token', res.json().get('refresh_token'))

        return res

    def refresh_token(self, refresh_token: str):
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": refresh_token
        }

        res = requests.post("https://kauth.kakao.com/oauth/token", data=data)

        if res.status_code == 200 and res.json().get('refresh_token'):
            # 결과값에 Refresh Token 이 있는 경우 기존 토큰 갱신
            # Refresh Token 은 만료 1달 전에 갱신
            from conf.caches import ka_ka_o_cache
            ka_ka_o_cache.set('refresh_token', res.json().get('refresh_token'))

        return res
