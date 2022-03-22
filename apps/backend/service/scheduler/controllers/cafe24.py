def schedule_cafe24_refresh_token():
    from conf.settings.prod import settings
    from conf.caches import cafe24_cache
    from apps.backend.external.cafe24.controllers.token import Token

    res = Token().refresh_token(cafe24_cache.get('refresh_token'))
    if res.status_code == 200:
        from apps.backend.service.notice.controllers.send import send_slack_background_task
        from apps.backend.service.notice.schemas import SendSlackRequest

        # 정상적으로 발급한 경우 적용
        access_token = res.json().get('access_token')
        refresh_token = res.json().get('refresh_token')
        version = cafe24_cache.get('version')

        # 메모리 저장
        cafe24_cache.set('access_token', access_token)
        cafe24_cache.set('refresh_token', refresh_token)
        cafe24_cache.set('version', version)

        # 슬랙 전송
        send_slack_background_task(SendSlackRequest(
            room='token',
            message=(
                '[ 카페24 토큰 정보 ]\n\n'
                f'- access_token : {access_token}\n'
                f'- refresh_token : {refresh_token}\n'
                f'- version : {version}'
            )
        ))

    if res.status_code != 200 and res.json().get('error') in ['invalid_grant', 'invalid_request']:
        # 토큰이 올바르지 않은 경우 토큰 적용
        cafe24_cache.set('refresh_token', settings.CAFE24_LOU_2_DEFAULT_REFRESH_TOKEN)
        cafe24_cache.set('version', settings.CAFE24_LOU_2_DEFAULT_VERSION)
        schedule_cafe24_refresh_token()

    res.raise_for_status()
