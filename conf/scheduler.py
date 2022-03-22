from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from conf.settings.prod import settings

job_stores = {
    "default": SQLAlchemyJobStore(url=settings.JOBS_SQLITE_URL)
}
executors = {
    "default": ThreadPoolExecutor(10)
}

job_defaults = {
    "coalesce": False,
    "max_instances": 5
}

Schedule = BackgroundScheduler(
    jobstores=job_stores,
    executors=executors,
    job_defaults=job_defaults
)

Schedule.start()
