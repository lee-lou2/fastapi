from celery import Celery
from celery.utils.log import get_task_logger

from apps.backend.service.notice.schemas import SendSlackRequest, SendEmailListRequest, SendEmailIn
from conf.settings.prod import settings

# Celery App
app = Celery(
    'tasks',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)
celery_log = get_task_logger(__name__)


@app.task
def health():
    return {"message": "Live"}


@app.task
def send_slack_task(message: str, room: str = 'alarm'):
    from apps.backend.service.notice.controllers.send import send_slack_background_task
    send_slack_background_task(SendSlackRequest(
        room=room,
        message=message
    ))


@app.task
def send_ka_ka_o_task(message: str):
    from conf.caches import ka_ka_o_cache
    from apps.backend.external.kakao.controllers.message import MessageTemplate, send_to_you_message

    access_token = ka_ka_o_cache.get('access_token')
    template = MessageTemplate.default_text(message)
    send_to_you_message(
        access_token,
        template
    )


@app.task
def send_email_task(message: str):
    # 이메일 발송
    from conf.settings.prod import settings
    from apps.backend.service.notice.controllers.send import send_email_background_task
    send_email_background_task(SendEmailListRequest(
        subject='알림이 도착하였습니다',
        message=message,
        users=[SendEmailIn(email=settings.RECEIVE_EMAIL_ADDRESS)]
    ))


@app.task
def upload_images_task(image_urls: list):
    import os
    import ftplib
    import datetime
    import requests
    from conf.settings.prod import settings

    count = 0

    for image_url in image_urls:
        image_url = str(image_url).strip() if image_url else None
        if image_url is None or not (image_url[:4] == 'http'):
            continue

        res = requests.get(image_url, allow_redirects=True)

        now = datetime.datetime.now()
        str_now = datetime.datetime.strftime(now, '%Y%m%d%H%M%S')
        file_path = f'image_{str_now}_{count}.jpg'
        count += 1

        open(file_path, 'wb').write(res.content)

        session = ftplib.FTP()
        session.connect(settings.FTP_CONNECT_URL, 21)
        session.login(settings.FTP_CONNECT_ID, settings.FTP_CONNECT_PASSWORD)

        upload_file = open(file_path, mode='rb')

        session.encoding = 'utf-8'
        session.storbinary('STOR ' + f'{settings.FTP_CONNECT_UPLOAD_PATH}{file_path}', upload_file)

        upload_file.close()

        session.quit()
        os.remove(file_path)
