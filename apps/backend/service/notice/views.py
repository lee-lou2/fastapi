from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from conf.router.deps import get_token
from core.authorization import BearerAccessToken
from .schemas import SendEmailListRequest, SendSMSRequest, SendSlackRequest
from apps.backend.auth.token.schemas import TokenDecodeOut
from .controllers.send import (
    send_email_background_task, send_sms_background_task, send_slack_background_task
)

# 라우터
router_v1 = APIRouter()


@router_v1.post("/email", dependencies=[Depends(BearerAccessToken())])
async def send_email(
        obj_in: SendEmailListRequest,
        background_tasks: BackgroundTasks,
        token: TokenDecodeOut = Depends(get_token),
) -> None:
    """
    이메일 발송
    :param obj_in:
    :param background_tasks:
    :param token:
    :return:
    """
    background_tasks.add_task(
        send_email_background_task,
        obj_in=obj_in
    )
    return None


@router_v1.post('/sms', dependencies=[Depends(BearerAccessToken())])
async def send_sms(
        obj_in: SendSMSRequest,
        background_tasks: BackgroundTasks,
        token: TokenDecodeOut = Depends(get_token),
) -> None:
    """
    문자 발송
    :param obj_in:
    :param background_tasks:
    :param token:
    :return:
    """
    background_tasks.add_task(
        send_sms_background_task,
        obj_in=obj_in
    )
    return None


@router_v1.post('/slack', dependencies=[Depends(BearerAccessToken())])
async def send_slack(
        obj_in: SendSlackRequest,
        background_tasks: BackgroundTasks,
        token: TokenDecodeOut = Depends(get_token),
) -> None:
    """
    슬랙 발송
    :param obj_in:
    :param background_tasks:
    :param token:
    :return:
    """
    background_tasks.add_task(
        send_slack_background_task,
        obj_in=obj_in
    )
    return None
