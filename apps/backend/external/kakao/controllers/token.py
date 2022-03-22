import requests


class Token:
    def __init__(self):
        from conf.settings.prod import settings
        self.client_id = settings.KAKAO_SEND_MESSAGE_CLIENT_ID
        self.redirect_url = settings.KAKAO_SEND_MESSAGE_REDIRECT_URL
        self.code = settings.KAKAO_SEND_MESSAGE_CODE
        self.scope = settings.KAKAO_SEND_MESSAGE_SCOPE

    def get_code(self):
        from selenium import webdriver

        # 셀레니움 정의
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/60.0.3112.50 Safari/537.36'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('user-agent={0}'.format(user_agent))
        driver = webdriver.Chrome('./chromedriver', options=options)

        url = f'https://kauth.kakao.com/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect_url}&response_type=code&scope={self.scope}'
        driver.get(url=url)
        # Todo 로그인 절차 진행 필요

        # 셀레니움을 이용해 코드 확인
        curr_url = driver.current_url
        return curr_url[curr_url.index("code=") + 5:] if curr_url and "code=" in curr_url else None

    def create_tokens(self):
        self.code = self.get_code() if self.code is None else self.code
        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_url,
            "code": self.code
        }
        res = requests.post(url, data=data)

        assert res.status_code == 200, '토큰 생성을 실패하였습니다'
        return res.json()

    def refresh_token(self, refresh_token: str):
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": refresh_token
        }

        return requests.post("https://kauth.kakao.com/oauth/token", data=data)
