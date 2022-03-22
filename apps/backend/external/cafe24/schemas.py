import json
from typing import Optional

from pydantic import BaseModel

from conf.settings.prod import settings
from core.consts import CAFE24_MY_MALL_DEFAULT_MARKET_B_CATEGORY_NUMBER
from core.convert.img_url_to_base64 import image_url_to_base64


# 전역 변수 지정
mall_name = settings.CAFE24_LOU_2_MALL_ID


class CreateProductOptionBase(BaseModel):
    has_option: str
    options: Optional[list]
    select_one_by_option: str

    def save(self, *args, **kwargs):
        # 신규 생성된 제품
        product_no = kwargs.pop('product_no')
        cafe24_api = kwargs.pop('cafe24_api')
        price = kwargs.pop('price')
        assert product_no and cafe24_api and price, '필수 파라미터가 없습니다'

        has_option = self.has_option

        # 옵션 정보
        option_list = []
        options_additional_information = []

        options = self.options
        if options and len(options) > 0:
            for option in options:
                option_detail_list = []

                # 데이터 조회
                option_name = option.get('option_name')
                option_value = option.get('option_value')
                required_option = option.get('required_option')

                if option_value and len(option_value) > 0:
                    for value in option_value:
                        option_text = value.get('option_text')
                        option_color = value.get('option_color')

                        additional_amount = value.get('additional_amount')
                        option_text = f'{option_text} (+{int(float(additional_amount))}원)' \
                            if additional_amount and int(float(additional_amount)) != 0 else option_text

                        # 옵션 세부 사항 생성
                        option_detail_list.append(
                            {
                                'option_text': option_text,
                                'option_color': option_color
                            }
                        )

                        # 추가 금이 없는 경우 다음으로 이동
                        if additional_amount is None or int(float(additional_amount)) == 0:
                            continue

                        additional_amount = float(int(float(additional_amount)) - int(float(price)))
                        # 옵션 추가금 리스트 생성
                        options_additional_information.append(
                            {
                                'option_name': option_name,
                                'option_text': option_text,
                                'additional_amount': additional_amount
                            }
                        )
                    # 옵션 리스트 생성
                    option_list.append(
                        {
                            'option_name': option_name,
                            'option_value': option_detail_list,
                            'option_display_type': "S",
                            'required_option': required_option
                        }
                    )

        if len(option_list) > 0 and len(list(filter(lambda x: x.get('required_option') == 'T', option_list))) == 0:
            # 필수 옵션이 없는 경우
            option_list.insert(
                0,
                {
                    'option_name': '제품',
                    'option_value': [{
                        'option_text': '단품'
                    }],
                    'option_display_type': 'S',
                    'required_option': 'T'
                }
            )

        option_data = {
            "request": {
                "has_option": has_option,
                "option_type": "F",
                "option_list_type": "C",
                "options": option_list
            }
        }
        option_url = f'https://{mall_name}.cafe24api.com/api/v2/admin/products/{product_no}/options'

        res = cafe24_api.request('POST', url=option_url, data=json.dumps(option_data))
        assert res.status_code == 201, res.text

        if len(options_additional_information) > 0:
            additional_amount_list = []
            # 코드 확인
            option_additional_url = f'https://{mall_name}.cafe24api.com/api/v2/admin/products/{product_no}/variants'
            res = cafe24_api.request('GET', url=option_additional_url)
            assert res.status_code == 200, res.text

            variants = res.json().get('variants')
            for option_additional_information in options_additional_information:
                option_name = option_additional_information.get('option_name')
                option_text = option_additional_information.get('option_text')
                additional_amount = option_additional_information.get('additional_amount')

                variant = list(filter(
                    lambda x: x.get('options') and len(x.get('options')) > 0 and x.get('options')[0].get(
                        'name') == option_name and x.get('options')[0].get('value') == option_text,
                    variants
                ))
                # 코드 조회 : 옵션명과 옵션 이름이 조회되지 않거나 2개 이상 조회되는 경우 None 처리
                variant_code = variant[0].get('variant_code') if variant and len(variant) == 1 else None
                # 코드가 확인되지 않는 경우 다음으로 이동
                if variant_code is None:
                    continue

                additional_amount_list.append(
                    {
                        "variant_code": variant_code,
                        "additional_amount": str(additional_amount)
                    }
                )

            if len(additional_amount_list) > 0:
                additional_amount_data = {
                    "requests": additional_amount_list
                }
                additional_amount_url = f'https://{mall_name}.cafe24api.com/api/v2/admin/products/{product_no}/variants'
                res = cafe24_api.request('PUT', url=additional_amount_url, data=json.dumps(additional_amount_data))
                assert res.status_code == 200, res.text


class CreateProductBase(BaseModel):
    product_no: int
    product_name: str
    options: CreateProductOptionBase
    supply_price: float
    description: str
    price: Optional[float]
    retail_price: Optional[float]
    summary_description: Optional[str]
    simple_description: Optional[str]
    product_tag: Optional[str]
    shipping_fee_by_product: Optional[str]
    shipping_fee_type: Optional[str]
    shipping_rates: Optional[list]
    origin_classification: Optional[str]
    origin_place_no: Optional[int]
    origin_place_value: Optional[str]
    detail_image: Optional[str]
    additionalimages: Optional[list]

    def save(self, *args, **kwargs):
        import re
        from .controllers.requests import Cafe24API
        from core.consts import CAFE24_MY_MALL

        # 상품 코드
        custom_product_code = self.product_no
        # 상품명
        product_name = self.product_name
        # 상품 공급가
        supply_price = float(self.supply_price)
        # 상세페이지
        description = self.description
        # 필수 항목
        product = {
            'display': 'T',  # 진열중
            'selling': 'T',  # 판매중
            'custom_product_code': custom_product_code,
            'product_name': product_name,
            'supply_price': supply_price,
            # 'use_naverpay': 'T',  # 네이버페이 사용
            # 'naverpay_type': 'C',  # 네이버페이, 몰 동시 판매
            'description': description,
            'shipping_scope': 'A',  # 국내 배송
            'shipping_method': '01',  # 택배
            'shipping_period': {  # 배송 기간
                "minimum": 1,
                "maximum": 3
            },
            'prepaid_shipping_fee': 'P',  # 배송비 선결제
            'add_category_no': [{'category_no': CAFE24_MY_MALL_DEFAULT_MARKET_B_CATEGORY_NUMBER}]
        }
        # 상품 판매가
        float_regex = r'^-?\d+(?:\.\d+)$'
        price = self.price
        if price and re.match(float_regex, str(price)):
            product['price'] = float(price)
        # 상품 소비자가
        retail_price = self.retail_price
        if retail_price and re.match(float_regex, str(retail_price)):
            product['retail_price'] = float(retail_price)
        # 상품요약설명
        summary_description = self.summary_description
        if summary_description:
            product['simple_description'] = summary_description
        # 상품 간략 설명
        simple_description = self.simple_description
        if simple_description:
            product['summary_description'] = simple_description
        # 태그
        product_tag = self.product_tag
        if product_tag:
            product['product_tag'] = product_tag
        # 개별 배송 여부
        shipping_fee_by_product = self.shipping_fee_by_product
        if shipping_fee_by_product:
            product['shipping_fee_by_product'] = shipping_fee_by_product
        # 배송비 타입
        shipping_fee_type = self.shipping_fee_type
        if shipping_fee_type:
            product['shipping_fee_type'] = shipping_fee_type
        # 배송비
        shipping_fee = self.shipping_rates[0].get('shipping_fee') \
            if self.shipping_rates and len(self.shipping_rates) > 0 else None
        if shipping_fee:
            product['shipping_rates'] = [{'shipping_fee': shipping_fee}]
        # 원산지 종류
        origin_classification = self.origin_classification
        if origin_classification:
            product['origin_classification'] = origin_classification
        # 원산지 번호
        origin_place_no = self.origin_place_no
        if origin_place_no:
            product['origin_place_no'] = origin_place_no
        # 원산지 기타 정보
        origin_place_value = self.origin_place_value
        if origin_place_value:
            product['origin_place_value'] = origin_place_value

        # 카페24 API 생성
        cafe24_api = Cafe24API(CAFE24_MY_MALL)

        data = {'request': product}
        product_url = f'https://{mall_name}.cafe24api.com/api/v2/admin/products'

        res = cafe24_api.request('POST', url=product_url, data=json.dumps(data))
        assert res.status_code == 201, res.text

        # 제품 등록 완료
        new_product_no = res.json().get('product', {}).get('product_no')

        # 이미지 등록
        additionalimages = self.additionalimages
        if additionalimages and len(additionalimages) > 0:
            # 이미지 준비
            images = list(map(
                lambda x: f'data:image/jpg;base64,{image_url_to_base64(x.get("big")).decode("utf-8")}',
                additionalimages
            ))
            # 메인 이미지 추가
            detail_image_url = self.detail_image
            images.insert(0, f'data:image/jpg;base64,{image_url_to_base64(detail_image_url).decode("utf-8")}')
            images = images[:6]
            # 이미지 생성 URL
            main_image_url = f'https://{mall_name}.cafe24api.com/api/v2/admin/products/{new_product_no}/images'
            sub_images_url = f'https://{mall_name}.cafe24api.com/api/v2/admin/products/{new_product_no}/additionalimages'

            # 이미지 생성 데이터
            list_image = images.pop(0)
            detail_image = images.pop(0)
            main_image_data = {
                "request": {
                    "image_upload_type": "B",
                    "detail_image": detail_image,
                    "list_image": list_image,
                    "tiny_image": list_image,
                    "small_image": detail_image
                }
            } if len(images) > 0 else None
            sub_images_data = {
                "request": {
                    "additional_image": images
                }
            }

            # 이미지 생성 요청
            res = cafe24_api.request('POST', url=main_image_url, data=json.dumps(main_image_data))
            assert res.status_code == 201, res.text

            res = cafe24_api.request('POST', url=sub_images_url, data=json.dumps(sub_images_data))
            assert res.status_code == 201, res.text

        # 옵션 생성
        self.options.save(
            product_no=new_product_no,
            cafe24_api=cafe24_api,
            price=price
        )


class CreateProductRequestBase(BaseModel):
    product_no: str

    @property
    def product_detail(self):
        product_no = self.product_no
        from .controllers.requests import Cafe24API
        cafe24_api = Cafe24API()
        return cafe24_api.retrieve_product(product_no=product_no)

    def save(self):
        product = self.product_detail.get('product')
        if product is None:
            raise
        product_base = CreateProductBase(**product)
        product_base.save()
        return True

    class Config:
        schema_extra = {
            "example": {
                "product_no": "<PRODUCT_NO>",
            }
        }
