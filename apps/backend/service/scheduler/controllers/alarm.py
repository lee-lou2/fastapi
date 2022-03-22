from datetime import datetime, timedelta

import pytz


def notification(message):
    from conf.celery import send_slack_task, send_email_task

    message = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    # 슬랙 전송
    send_slack_task.delay(message)
    # # 이메일 발송
    # send_email_task.delay(message)


def schedule_alarm_service():
    from conf.databases import DefaultSession
    from apps.backend.chatbot.alarm.models import ChatBotAlarm
    from apps.backend.chatbot.base.models import ChatBotContent
    # 데이터 베이스 생성
    db = DefaultSession()

    # 유효한 알림 생성
    now = datetime.now().astimezone(pytz.timezone('Asia/Seoul'))
    qs = db.query(ChatBotAlarm).filter(ChatBotAlarm.next_alarm < now)
    for alarm in qs:
        if alarm.last_alarm is not None:
            continue
        next_alarm = alarm.next_alarm + timedelta(minutes=alarm.time_interval)
        alarm.next_alarm = next_alarm
        content_id = alarm.chat_bot_content_id
        content = db.query(ChatBotContent).filter_by(id=content_id).first()
        # 알림
        notification(f'{content.content} | 다음 알림 [{next_alarm}] | ID [{alarm.id}]')
    db.commit()
    db.close()
