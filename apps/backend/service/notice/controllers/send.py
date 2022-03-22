import base64
import hashlib
import hmac
import json
import time

import requests

from conf.celery import app
from conf.settings.prod import settings
from ..schemas import SendEmailListRequest, SendSMSRequest, SendSlackRequest


def send_email_background_task(obj_in: SendEmailListRequest):
    """
    이메일 발송
    :param obj_in:
    :return:
    """
    import smtplib
    from email.mime.text import MIMEText

    # 변수 지정
    subject = obj_in.subject
    message = obj_in.message
    users = obj_in.users

    smtp = smtplib.SMTP('ecsmtp.cafe24.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)

    for user in users:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['To'] = user.email
        smtp.sendmail(settings.EMAIL_ADDRESS, user.email, msg.as_string())

    smtp.quit()
    return True


def send_sms_background_task(obj_in: SendSMSRequest):
    """
    문자 발송
    :param obj_in:
    :return:
    """
    # 변수 지정
    message = obj_in.message
    phone = obj_in.phone

    sms_uri = "/sms/v2/services/{}/messages".format(settings.NAVER_CLOUD_SID)
    sms_url = "https://sens.apigw.ntruss.com{}".format(sms_uri)

    start_time = int(float(time.time()) * 1000)

    hash_str = "POST {}\n{}\n{}".format(
        sms_uri,
        start_time,
        settings.NAVER_CLOUD_ACCESS_KEY_ID
    )

    digest = hmac.new(
        settings.NAVER_CLOUD_ACCESS_SECRET_KEY,
        msg=hash_str.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    d_hash = base64.b64encode(digest).decode()

    msg_data = {
        'type': 'SMS',
        'countryCode': '82',
        'from': "{}".format(settings.SMS_FROM_NO),
        'contentType': 'COMM',
        'content': "{}".format(message),
        'messages': [{'to': "{}".format(phone)}]
    }

    res = requests.post(
        sms_url, data=json.dumps(msg_data),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": str(start_time),
            "x-ncp-iam-access-key": settings.NAVER_CLOUD_ACCESS_KEY_ID,
            "x-ncp-apigw-signature-v2": d_hash
        }
    )
    res.raise_for_status()
    return True


def send_slack_background_task(obj_in: SendSlackRequest):
    # 변수 지정
    room = obj_in.room
    message = obj_in.message

    # 메시지 전송
    requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + settings.SLACK_KEY},
        data={"channel": room, "text": message}
    )
    return True
