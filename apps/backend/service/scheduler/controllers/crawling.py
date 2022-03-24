def notification(message: str):
    from conf.celery import send_slack_task
    send_slack_task.delay(message)

    from conf.caches import ka_ka_o_cache
    from apps.backend.external.kakao.controllers.message import MessageTemplate, send_to_you_message

    access_token = ka_ka_o_cache.get('access_token')
    template = MessageTemplate.default_text(message)
    send_to_you_message(
        access_token,
        template
    )


def crawling_data():
    import re
    import json
    import urllib.request
    from conf.settings.prod import settings
    from conf.caches import crawling_cache

    client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_CLIENT_SECRET
    enc_text = urllib.parse.quote(settings.NAVER_DEFAULT_SEARCH_TEXT)
    urls = [
        f"https://openapi.naver.com/v1/search/blog?query={enc_text}&display=100&start=1&sort=date",
        f"https://openapi.naver.com/v1/search/cafearticle.json?query={enc_text}&display=100&start=1&sort=date",
        f"https://openapi.naver.com/v1/search/news.json?query={enc_text}&display=100&start=1&sort=date"
    ]
    items = []
    for url in urls:
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        res_code = response.getcode()
        if res_code == 200:
            response_body = response.read()
            response_dict = json.loads(response_body.decode('utf-8'))
            for item in response_dict.get('items'):
                # 마지막 링크 확인
                if crawling_cache.exists(item.get('link')):
                    crawling_cache.delete(item.get('link'))
                    break
                description = re.sub('(<([^>]+)>)', '', item.get('description'))
                items.append({'description': description})
            crawling_cache.set(response_dict.get('items')[0].get('link'), '')
        else:
            notification("Error Code:" + res_code)
            break
    else:
        from conf.databases import mongo
        collection = mongo.information
        collection.insert_many(items)
        # notification(f'[{settings.NAVER_DEFAULT_SEARCH_TEXT}] {len(items)}개 추가 완료')
