from sqlalchemy import Column, String

from conf.databases import DefaultBase


class DataApartmentSales(DefaultBase):
    """
    아파트 매매 정보
    """
    # 거래금액
    price = Column(String, nullable=True)
    # 거래유형
    sales_type = Column(String, nullable=True)
    # 건축년도
    construction_year = Column(String, nullable=True)
    # 년
    year = Column(String, nullable=True)
    # 법정동
    dong = Column(String, nullable=True)
    # 아파트
    apartment = Column(String, nullable=True)
    # 월
    month = Column(String, nullable=True)
    # 일
    day = Column(String, nullable=True)
    # 전용면적
    area = Column(String, nullable=True)
    # 중개사소재지
    intermediary = Column(String, nullable=True)
    # 지번
    lot_number = Column(String, nullable=True)
    # 지역코드
    gu_code = Column(String, nullable=True)
    # 층
    floor = Column(String, nullable=True)
    # 해제사유발생일
    termination_at = Column(String, nullable=True)
    # 해제여부
    is_termination = Column(String, nullable=True)
    # 인덱스
    uid = Column(String, nullable=False, unique=True)
