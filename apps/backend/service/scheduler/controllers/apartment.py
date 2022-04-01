import re

import pytz
import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from hangul_utils import split_syllables

from apps.backend.service.scheduler.models import DataApartmentSales
from conf.databases import DefaultSession
from conf.settings.prod import settings
from core.choices import ApartmentSalesFormatChoices
from core.consts import KOR_ENG_TABLE


class ApartmentSalesAPI:
    def __init__(self, gu_code: str = None, duplicate: bool = False):
        self.code = None
        self.db = DefaultSession()
        self.gu_code = gu_code if gu_code else settings.DATA_API_DEFAULT_GU_CODE
        self.now = datetime.now().astimezone(pytz.timezone('Asia/Seoul')) - timedelta(days=1)
        self.base_date = self.now.strftime("%Y%m")
        self.service_key = settings.DATA_API_SERVICE_KEY
        self.url = settings.DATA_API_SERVICE_URL

    def set_gu_code(self, gu_name):
        """
        구 코드 적용
        """
        gu_code = self.code[(self.code['name'].str.contains(gu_name))]
        gu_code = gu_code['code'].reset_index(drop=True)
        self.gu_code = gu_code

    def _get_data(self):
        """
        데이터 조회
        """
        return requests.get(
            f'{self.url}LAWD_CD={self.gu_code}&DEAL_YMD={self.base_date}&serviceKey={self.service_key}'
        )

    def _create_id(self, str_id: str):
        """
        한글 인덱스 영어로 변환
        """
        split_text = split_syllables(str_id)
        return ''.join(
            [
                word.replace(word, KOR_ENG_TABLE[word])
                if KOR_ENG_TABLE.get(word) else word
                for word in str(split_text)
            ]
        )

    def get_items(self, _format: str) -> list:
        """
        조회된 데이터 타입 변환
        """
        # 데이터 조회
        response = self._get_data()

        # 데이터 변환
        root = ET.fromstring(response.content)
        item_list = []

        for child in root.find('body').find('items'):
            elements = child.findall('*')
            data, idx = {}, ''

            for element in elements:
                tag = element.tag.strip()
                text = element.text.strip()
                data[tag] = text
                idx += str(tag) + str(text)

            # 인덱스로 사용할 텍스트 설정
            eng_id = self._create_id(re.sub('[^A-Za-z0-9가-힣]', '', idx))
            data['id'] = eng_id

            # 이미 존재하는 경우 다음으로 이동
            if self.db.query(DataApartmentSales).filter_by(uid=eng_id).count() > 0:
                continue

            # 데이터 저장
            self.save(data)

            # 데이터 변환
            data.pop('지역코드')
            data.pop('중개사소재지')
            data['거래일'] = f"{data.pop('년')}-{data.pop('월')}-{data.pop('일')}"
            apartment = data.get('법정동') + '+' + data.get('아파트')
            apartment = apartment.strip().replace(' ', '+')

            # 반환 값 종합
            item_list.append((
                self.set_format(_format, data),
                apartment
            ))
        return item_list

    def save(self, instance: dict):
        """
        데이터 저장
        """
        obj = DataApartmentSales(
            price=instance.get('거래금액'),
            sales_type=instance.get('거래유형'),
            construction_year=instance.get('건축년도'),
            year=instance.get('년'),
            dong=instance.get('법정동'),
            apartment=instance.get('아파트'),
            month=instance.get('월'),
            day=instance.get('일'),
            area=instance.get('전용면적'),
            intermediary=instance.get('중개사소재지'),
            lot_number=instance.get('지번'),
            gu_code=instance.get('지역코드'),
            floor=instance.get('층'),
            termination_at=instance.get('해제사유발생일'),
            is_termination=instance.get('해제여부'),
            uid=instance.get('id')
        )
        self.db.add(obj)
        self.db.commit()

    @staticmethod
    def set_format(_format: str, data: dict):
        """
        변환 포맷 지정
        """
        set_format_data = data
        if _format == ApartmentSalesFormatChoices.K.value:
            set_format_data = ''.join([f'- {key} : {value}\n' for key, value in data.items() if key != 'id'])
        return set_format_data

    def send_notification(self, messages: list):
        """
        비동기 알람 전송
        """
        from conf.celery import send_slack_task, send_ka_ka_o_task

        # 검색용 링크
        link = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='

        for message in messages:
            message = message[0] + link + message[1]
            # 슬랙 전송
            send_slack_task.delay(message)
            # 카카오 전송
            send_ka_ka_o_task.delay(message)

    def run(self, _format: str):
        """
        실행
        """
        items = self.get_items(_format)
        self.send_notification(items)


def schedule_apartment_service():
    # 인근 지역 검색
    codes = ['11410', '11440', '11380']
    for code in codes:
        api = ApartmentSalesAPI(gu_code=code)
        api.run(ApartmentSalesFormatChoices.K.value)
