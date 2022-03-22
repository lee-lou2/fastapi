import enum


"""
[ enum 메뉴얼 ]
변수(name) = '값'(value)

* Example
class TestChoices(enum.Enum):
    A = 'apple'

TestChoices.A.name > 'A'
TestChoices.A.value > 'apple'
"""


class SocialTypeChoices(enum.Enum):
    G = 'google'
    A = 'apple'
    K = 'kakao'
    N = 'naver'
    L = 'local'


class ChatBotContentTypeChoices(enum.Enum):
    T = 'Text'
    IN = 'Int'
    P = 'Picture'
    D = 'Date'
    DT = 'DateTime'
    A = 'Alarm'
    DA = 'Delete Alarm'
