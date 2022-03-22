from conf.settings.prod import settings

EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc)"
MAX_API_KEY = 3
MAX_API_WHITELIST = 10

# 카페24 API
CAFE24_MARKET_B_MALL = settings.CAFE24_MARKET_B_MALL_ID
CAFE24_MY_MALL = settings.CAFE24_LOU_2_MALL_ID
CAFE24_MY_MALL_DEFAULT_MARKET_B_CATEGORY_NUMBER = 24

DEFAULT_KA_KA_O_RESPONSE_TEMPLATE = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "JAY 챗봇 동작중"
                        },
                        "items": [
                            {
                                "title": "",
                                "description": "",
                                "imageUrl": "",
                                "link": {
                                    "web": ""
                                }
                            }
                        ],
                        "buttons": []
                    }
                }
            ],
            "quickReplies": []
        }
    }