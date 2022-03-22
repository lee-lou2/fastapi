import requests


class Token:
    def __init__(self):
        from conf.settings.prod import settings
        self.mall = settings.CAFE24_LOU_2_MALL_ID
        self.client_id = settings.CAFE24_LOU_2_CLIENT_ID
        self.client_secret = settings.CAFE24_LOU_2_CLIENT_SECRET
        self.redirect_uri = settings.CAFE24_LOU_2_REDIRECT_URL
        self.master_id = settings.CAFE24_LOU_2_MASTER_ID
        self.master_password = settings.CAFE24_LOU_2_MASTER_PASSWORD

    def get_code_use_selenium(self):
        import time
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

        # 셀레니움을 이용해 로그인
        driver.get(url='https://eclogin.cafe24.com/Shop/')
        time.sleep(1)
        # 사용자 아이디
        ele = driver.find_element_by_id('mall_id')
        ele.send_keys(self.master_id)
        time.sleep(0.5)
        # 사용자 패스워드
        ele = driver.find_element_by_id('userpasswd')
        ele.send_keys(self.master_password)
        # 로그인 클릭
        driver.execute_script("form_check();")
        time.sleep(1)
        # 패스워드 변경 화면이 표시되는 경우 다음으로 이동
        curr_url = driver.current_url
        if curr_url == 'https://user.cafe24.com/comLogin/?action=comForce&req=hosting':
            ele = driver.find_element_by_id('iptBtnEm')
            ele.click()

        # 권한
        scope = '''
        mall.write_category, mall.read_category,
        mall.write_product, mall.read_product,
        mall.write_personal, mall.read_personal,
        mall.write_collection, mall.read_collection,
        mall.write_supply, mall.read_supply,
        mall.write_order, mall.read_order,
        mall.write_community, mall.read_community,
        mall.write_customer, mall.read_customer,
        mall.write_notification, mall.read_notification,
        mall.write_store, mall.read_store,
        mall.write_promotion, mall.read_promotion,
        mall.write_design, mall.read_design,
        mall.write_application, mall.read_application,
        mall.read_salesreport,
        mall.read_shipping, mall.write_shipping,
        mall.write_mileage,mall.read_mileage
        '''
        scope = scope.replace("\n", "").replace(" ", "").strip()

        url = f'https://marketb.cafe24api.com/api/v2/oauth/authorize?' \
              f'response_type=code&' \
              f'client_id={self.client_id}&' \
              f'redirect_uri={self.redirect_uri}&' \
              f'scope={scope}'

        # 셀레니움을 이용해 코드 확인
        driver.get(url=url)
        curr_url = driver.current_url
        return curr_url[curr_url.index("code=") + 5:curr_url.index("&")] if curr_url else None

    @property
    def headers(self):
        import base64

        client_keys = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode('utf-8')
        ).decode('utf-8')

        return {
            'Authorization': f'Basic {client_keys}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    def create_access_token(self, code: str):
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        res = requests.post(f'https://{self.mall}.cafe24api.com/api/v2/oauth/token', headers=self.headers, data=data)
        assert res.status_code == 200, '토큰 생성을 실패하였습니다'
        return res.json()

    def refresh_token(self, refresh_token: str):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }

        return requests.post(f'https://{self.mall}.cafe24api.com/api/v2/oauth/token', headers=self.headers, data=data)
