from fastapi import APIRouter, Request
from conf.databases import es
from core.templates import template

router_v1 = APIRouter()


@router_v1.get("/")
async def memo(
        *,
        request: Request,
        friend_key: str = None,
        q: str = None,
):
    from conf.caches import memo_cache

    # 캐시에 저장되어있는지 확인
    if memo_cache.exists(friend_key):
        objs = es.search(index='chat_bot', body={
            'from': 0,
            'size': 100,
            'query': {
                'match': {
                    'message': q
                }
            }
        }).get('hits', {}).get('hits')
        memo_list = [(obj.get('_source', {}).get('message'), obj.get('_source', {}).get('id')) for obj in objs]
    else:
        from core import exceptions as ex
        raise ex.FrontendExceptions.ExpiredFriend
    return template.init.TemplateResponse(
        "chatbot/memo.html",
        {
            "request": request,
            "memo_list": memo_list
        }
    )
