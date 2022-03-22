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
def send_slack_task(message: str):
    from apps.backend.service.notice.controllers.send import send_slack_background_task
    send_slack_background_task(SendSlackRequest(
        room='alarm',
        message=message
    ))


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
