import json
import requests


def send_to_me_message(access_token: str, template: dict):
    """
    나에게 메시지 보내기
    """
    header = {"Authorization": 'Bearer ' + access_token}
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    data = {"template_object": json.dumps(template)}
    return requests.post(url, headers=header, data=data)


class MessageTemplate:
    @classmethod
    def default_text(cls, message):
        return {
            'object_type': 'text',
            'text': message,
            'link': {
                'web_url': '',
                'mobile_web_url': ''
            }
        }
