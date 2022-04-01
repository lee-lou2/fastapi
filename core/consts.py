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

# 한글-영어 변환
KOR_WORDS = list('ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
ENG_WORDS = [
    'r', 'R', 'rt', 's', 'sw', 'sg', 'e', 'f', 'fr', 'fa', 'fq', 'ft',
    'fx', 'fv', 'fg', 'a', 'q', 'qt', 't', 'T', 'd', 'w', 'c', 'z',
    'x', 'v', 'g', 'k', 'o', 'i', 'O', 'j', 'p', 'u', 'P', 'h', 'hk',
    'ho', 'hl', 'y', 'n', 'nj', 'np', 'nl', 'b', 'm', 'ml', 'l'
]
KOR_ENG_TABLE = dict(zip(KOR_WORDS, ENG_WORDS))