from fastapi import APIRouter

from apps.backend.service.scheduler.schemas import ScheduleName
from conf.scheduler import Schedule
from .models import *


# 라우터
router_v1 = APIRouter()


@router_v1.get("/schedule")
async def get_scheduled_syncs():
    return [
        {
            "Name": str(job.id),
            "Run Frequency": str(job.trigger),
            "Next Run": str(job.next_run_time)
        }
        for job in Schedule.get_jobs()
    ]


@router_v1.post("/schedule", status_code=201)
async def add_schedule(
        time_in_seconds: int = 60,
        schedule_name: ScheduleName = None
):
    schedule_job = None
    if schedule_name == ScheduleName.CAFE24_REFRESH_TOKEN:
        from apps.backend.service.scheduler.controllers.cafe24 import schedule_cafe24_refresh_token
        schedule_job = Schedule.add_job(
            schedule_cafe24_refresh_token,
            'interval',
            seconds=time_in_seconds,
            id='cafe24_refresh_token'
        )
    elif schedule_name == ScheduleName.KAKAO_REFRESH_TOKEN:
        from apps.backend.service.scheduler.controllers.kakao import schedule_ka_ka_o_refresh_token
        schedule_job = Schedule.add_job(
            schedule_ka_ka_o_refresh_token,
            'interval',
            seconds=time_in_seconds,
            id='kakao_refresh_token'
        )
    elif schedule_name == ScheduleName.SEND_STOCK:
        from apps.backend.service.scheduler.controllers.stock import schedule_send_stock
        schedule_job = Schedule.add_job(
            schedule_send_stock,
            'interval',
            seconds=time_in_seconds,
            id='send_stock'
        )
    elif schedule_name == ScheduleName.ALARM_SERVICE:
        from apps.backend.service.scheduler.controllers.alarm import schedule_alarm_service
        schedule_job = Schedule.add_job(
            schedule_alarm_service,
            'interval',
            seconds=time_in_seconds,
            id='alarm_service'
        )
    elif schedule_name == ScheduleName.CRAWLING:
        from apps.backend.service.scheduler.controllers.crawling import crawling_data
        schedule_job = Schedule.add_job(
            crawling_data,
            'interval',
            seconds=time_in_seconds,
            id='crawling'
        )
    elif schedule_name == ScheduleName.APARTMENT_SALES_API:
        from apps.backend.service.scheduler.controllers.apartment import schedule_apartment_service
        schedule_job = Schedule.add_job(
            schedule_apartment_service,
            'interval',
            seconds=time_in_seconds,
            id='apartment_sales_api'
        )
    return {
        "Scheduled": True,
        "JobID": schedule_job.id,
    } if schedule_job else None


@router_v1.delete("/schedule", status_code=204)
async def remove_schedule(
        schedule_name: ScheduleName = None
):
    if schedule_name == ScheduleName.CAFE24_REFRESH_TOKEN:
        Schedule.remove_job('cafe24_refresh_token')
        return {
            "Scheduled": False,
            "JobID": 'cafe24_refresh_token'
        }
    elif schedule_name == ScheduleName.KAKAO_REFRESH_TOKEN:
        Schedule.remove_job('kakao_refresh_token')
        return {
            "Scheduled": False,
            "JobID": 'kakao_refresh_token'
        }
    elif schedule_name == ScheduleName.SEND_STOCK:
        Schedule.remove_job('send_stock')
        return {
            "Scheduled": False,
            "JobID": 'send_stock'
        }
    elif schedule_name == ScheduleName.ALARM_SERVICE:
        Schedule.remove_job('alarm_service')
        return {
            "Scheduled": False,
            "JobID": 'alarm_service'
        }
    elif schedule_name == ScheduleName.CRAWLING:
        Schedule.remove_job('crawling')
        return {
            "Scheduled": False,
            "JobID": 'crawling'
        }
    elif schedule_name == ScheduleName.APARTMENT_SALES_API:
        Schedule.remove_job('apartment_sales_api')
        return {
            "Scheduled": False,
            "JobID": 'apartment_sales_api'
        }
