import json

import pytz
from sqlalchemy.orm import Session


class KaKaoProperty:
    """
    카카오 챗봇 반환 값 조회
    """
    def __init__(self, body: bytes, db: Session = None, block_type: str = None):
        """
        데이터 가져온 후 변환
        :param body:
        """
        from core.utils.dict import DepthOfDictionary
        import json
        self.db = db
        self._data = json.loads(body)
        self.depth_of_dict = DepthOfDictionary(self._data)
        self.content = None
        self.block_type = block_type
        self.is_created = False

    @property
    def data(self) -> dict:
        return self._data

    @property
    def bot(self) -> dict:
        # 봇 정보
        return {'bot_id': self.depth_of_dict.get_value('userRequest', 'user', 'id')}

    @property
    def text(self) -> dict:
        # 알림
        if self.depth_of_dict.get_value('intent', 'name') in ['Create Alarm', 'Delete Alarm']:
            return {'text': self.depth_of_dict.get_value('action', 'params', 'content')}
        # 폴백
        return {'text': self.depth_of_dict.get_value('userRequest', 'utterance')}

    @property
    def block(self) -> dict:
        # 블록 정보
        return {
            'block_id': self.depth_of_dict.get_value('intent', 'id'),
            'block_name': self.depth_of_dict.get_value('intent', 'name'),
        }

    @property
    def friend(self) -> dict:
        # 사용자 정보
        friend = self.depth_of_dict.get_value('userRequest', 'user', 'properties')
        friend = friend if friend else {}
        return {
            'is_friend': friend.get('botUserKey'),
            'user_key': friend.get('bot_user_key')
        }

    @property
    def datetime(self, param_name: str) -> dict:
        # 날짜 정보
        assert param_name, "필수 파라미터가 포함되어있지 않습니다."
        date = self.depth_of_dict.get_value('action', 'params', param_name)
        date = json.loads(date).get('value') if date else None
        return {'date': date}

    @property
    def picture(self, param_name: str) -> dict:
        # 이미지 정보
        assert param_name, "필수 파라미터가 포함되어있지 않습니다."
        picture = self.depth_of_dict.get_value('action', 'params', param_name)
        picture = json.loads(picture) if picture else {}
        return {'pictures': picture.get('secureUrls')}

    def create_image(self, content):
        # 이미지 파일 조회
        image_file_param = self.depth_of_dict.get_value('action', 'params', 'image_file')
        image_file_param = json.loads(image_file_param).get('secureUrls') if image_file_param else None
        image_file_param = str(image_file_param)[5:-1] if image_file_param else None
        image_file_params = image_file_param.split(',')

        # 이미지 링크 조회
        image_url_param = self.depth_of_dict.get_value('action', 'params', 'image_url')

        image_urls = [image_url_param] + image_file_params

        from conf.celery import upload_images_task
        upload_images_task.delay(image_urls=image_urls)

        self.is_created = True

    def create_alarm(self, content):
        """
        알림 생성
        """
        from apps.backend.chatbot.alarm.models import ChatBotAlarm
        created_param = self.depth_of_dict.get_value('action', 'params', 'created')
        created = json.loads(created_param).get('value') if created_param else None
        time_interval = self.depth_of_dict.get_value('action', 'params', 'time_interval')
        if not (created and time_interval):
            raise

        # 생성일 변환
        import datetime
        from apps.backend.service.scheduler.controllers.alarm import notification
        created = datetime.datetime.strptime(created, '%Y-%m-%dT%H:%M:%S')

        # 간격 변환
        try:
            time_interval = eval(str(time_interval))
            time_interval = int(time_interval) if str(time_interval).isdecimal() else 1

            alarm = ChatBotAlarm(
                time_interval=time_interval,
                next_alarm=created,
                chat_bot_content=content
            )
            self.db.add(alarm)
            self.db.commit()
            notification(f'{content.content}, 알림이 생성 되었습니다. | 알람 시작 [{created}] | ID [{alarm.id}]')
            self.is_created = True
        except Exception as ex:
            notification(f'{content.content}, 알림이 생성이 중단되었습니다. | 오류 : {ex}')

    def delete(self):
        # 알람 서비스
        import datetime
        from apps.backend.chatbot.alarm.models import ChatBotAlarm
        from core.choices import ChatBotContentTypeChoices
        if self.block_type == ChatBotContentTypeChoices.DA.name:
            alarm_id = self.text.get('text')
            alarm = self.db.query(ChatBotAlarm).filter_by(id=alarm_id).first()
            if alarm and alarm.last_alarm is None:
                alarm.last_alarm = datetime.datetime.now().astimezone(pytz.timezone('Asia/Seoul'))
                self.db.commit()
                from apps.backend.service.scheduler.controllers.alarm import notification
                notification(f'[{alarm_id}] 알림이 삭제 되었습니다.')

    def save(self, add_props: list = None):
        self.save_default()
        self.save_additional(add_props)

    def save_default(self):
        """
        bot, block, friend, text
        :return:
        """
        from apps.backend.chatbot.base.models import (
            ChatBot, ChatBotContent
        )
        friend_key = self.friend.get('user_key')
        content = self.text.get('text')
        chat_bot = self.db.query(ChatBot).filter_by(friend_key=friend_key).first()
        if chat_bot is None:
            chat_bot = ChatBot(
                friend_key=friend_key
            )
            self.db.add(chat_bot)
        chat_bot_content = ChatBotContent(
            chat_bot=chat_bot,
            content=content
        )
        if self.block_type:
            chat_bot_content.block_type = self.block_type
        self.db.add(chat_bot_content)
        self.db.commit()

        # --------------------------
        # Content Type 에 대한 추가 처리
        # --------------------------
        # Type : 이미지
        media_content_type = self.depth_of_dict.get_value('userRequest', 'params', 'media', 'type')
        if media_content_type and media_content_type == 'image':
            from conf.celery import upload_images_task
            upload_images_task.delay(image_urls=[content])

        # ------------------------
        # Block Type 에 대한 추가 처리
        # ------------------------
        # Type : 알람
        from core.choices import ChatBotContentTypeChoices
        if self.block_type == ChatBotContentTypeChoices.A.name:
            self.create_alarm(chat_bot_content)
        # Type : 이미지
        elif self.block_type == ChatBotContentTypeChoices.IMG.name:
            self.create_image(chat_bot_content)

        # ----------
        # 기타 추가 처리
        # ----------
        # 엘라스틱 서치
        from conf.databases import es
        es_index = 'chat_bot'
        if not es.indices.exists(index=es_index):
            es.indices.create(index=es_index)
        doc = {
            'friend_key': friend_key,
            'message': content,
            'id': chat_bot_content.id
        }
        es.index(index=es_index, doc_type='_doc', body=doc)
        es.indices.refresh(index=es_index)

        # 반환 값 설정
        self.content = content

    def save_additional(self, add_props: list):
        pass
