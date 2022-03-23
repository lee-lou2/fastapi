from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from conf.databases import get_db, es
from apps.backend.chatbot.base.models import *

# 라우터
router_v1 = APIRouter()


def add_content(body: bytes, db: Session):
    from apps.backend.chatbot.base.controllers.properties import KaKaoProperty
    prop = KaKaoProperty(body, db)
    prop.save()
    return prop.content


@router_v1.get("/", status_code=200)
async def get_memo(
        q: str,
        size: int = 10
):
    return es.search(index='chat_bot', body={
        'from': 0,
        'size': size,
        'query': {
            'match': {
                'message': q
            }
        }
    }).get('hits', {}).get('hits')


@router_v1.post("/list/", status_code=200)
async def memo_list(
        *,
        request: Request,
        db: Session = Depends(get_db)
):
    from conf.caches import memo_cache
    from apps.backend.chatbot.base.controllers.properties import KaKaoProperty

    body = await request.body()
    prop = KaKaoProperty(body, db)
    friend_key = prop.friend.get('user_key')
    url = f'http://{settings.DEFAULT_DOMAIN}/frontend/chat_bot/memo/?friend_key={friend_key}'

    # 3분 후 삭제되도록 캐시 설정
    memo_cache.set(friend_key, '', 180)

    from core.consts import DEFAULT_KA_KA_O_RESPONSE_TEMPLATE
    response = DEFAULT_KA_KA_O_RESPONSE_TEMPLATE
    response['template']['outputs'][0]['listCard']['items'][0]['title'] = '링크가 생성되었습니다.'
    response['template']['outputs'][0]['listCard']['items'][0]['description'] = ': 생성된 링크는 3분 동안만 접속이 가능합니다'
    response['template']['outputs'][0]['listCard']['buttons'].append({
        "label": "이동하기",
        "action": "webLink",
        "webLinkUrl": url
    })
    return response


@router_v1.post("/", status_code=201)
async def create_memo(
        *,
        request: Request,
        db: Session = Depends(get_db)
):
    body = await request.body()
    # 데이터 저장
    content = add_content(body, db)

    from core.consts import DEFAULT_KA_KA_O_RESPONSE_TEMPLATE
    response = DEFAULT_KA_KA_O_RESPONSE_TEMPLATE
    response['template']['outputs'][0]['listCard']['items'][0]['title'] = '데이터가 저장되었습니다.'
    response['template']['outputs'][0]['listCard']['items'][0]['description'] = ': ' + content
    return response
