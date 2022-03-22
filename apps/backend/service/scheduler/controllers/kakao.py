def schedule_ka_ka_o_refresh_token():
    from conf.settings.prod import settings
    from conf.caches import ka_ka_o_cache
    from apps.backend.external.kakao.controllers.token import Token

    res = Token().refresh_token(ka_ka_o_cache.get('refresh_token'))
    if res.status_code == 200:
        from apps.backend.service.notice.controllers.send import send_slack_background_task
        from apps.backend.service.notice.schemas import SendSlackRequest

        # 정상적으로 발급한 경우 적용
        access_token = res.json().get('access_token')

        # 메모리 저장
        ka_ka_o_cache.set('access_token', access_token)

        # 슬랙 전송
        send_slack_background_task(SendSlackRequest(
            room='token',
            message=(
                '[ 카카오 토큰 정보 ]\n\n'
                f'- access_token : {access_token}\n'
            )
        ))

    if res.status_code != 200 and res.json().get('error_code') == 'KOE319':
        # 토큰이 올바르지 않은 경우 토큰 적용
        ka_ka_o_cache.set('refresh_token', settings.KAKAO_MESSAGE_DEFAULT_REFRESH_TOKEN)
        schedule_ka_ka_o_refresh_token()

    res.raise_for_status()
