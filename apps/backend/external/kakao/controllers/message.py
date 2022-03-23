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


def send_to_you_message(access_token: str, template: dict):
    """
    타인에게 메시지 보내기
    """
    from conf.settings.prod import settings
    uuid = settings.KAKAO_MY_UUID
    header = {"Authorization": 'Bearer ' + access_token}
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    data = {
        "receiver_uuids": f'["{uuid}"]',
        "template_object": json.dumps(template)
    }
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
