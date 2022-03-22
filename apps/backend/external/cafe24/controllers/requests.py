import requests

from core.consts import CAFE24_MARKET_B_MALL, CAFE24_MY_MALL


class Cafe24API:
    def __init__(self, mall=CAFE24_MARKET_B_MALL):
        self.mall = mall
        self.token = None
        self.version = None
        self.set_token_and_version()

    def set_token_and_version(self):
        from conf.caches import cafe24_cache
        self.token = cafe24_cache.get('access_token')
        self.version = cafe24_cache.get('version')

    def get_token_and_version(self):
        if self.mall == CAFE24_MARKET_B_MALL:
            from conf.settings.prod import settings

            res = requests.get(settings.CAFE24_MARKET_B_TOKEN_URL)
            assert res.status_code == 200, '토큰을 가져오지 못했습니다.'

            token = res.json().get('result', {}).get('access_token')
            version = res.json().get('result', {}).get('version')
            return token, version
        elif self.mall == CAFE24_MY_MALL:
            return self.token, self.version
        return None, None

    @property
    def headers(self):
        token, version = self.get_token_and_version()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Cafe24-Api-Version": version,
        }

    def _get_or_raise(self, url):
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json()

    def _exists(self, product_no):
        url = f'https://{self.mall}.cafe24api.com/api/v2/admin/products/count?product_no={product_no}'
        res = self._get_or_raise(url)
        return res.get('count') == 1

    def retrieve_product(self, product_no, *args, **kwargs):
        assert self._exists(product_no), 'Not Found Product'
        url = f'https://{self.mall}.cafe24api.com/api/v2/admin/products/{product_no}?' \
              f'embed=options,additionalimages,variants'
        return self._get_or_raise(url)

    def request(self, method: str, url: str, data: str = None):
        res = requests.request(
            method=method,
            url=url,
            data=data,
            headers=self.headers
        )
        if res.status_code == 401 and \
                res.json().get('error').get('message') \
                == 'access_token time expired. (invalid_token)':
            self.set_token_and_version()
            res = requests.request(
                method=method,
                url=url,
                data=data,
                headers=self.headers
            )
        return res
