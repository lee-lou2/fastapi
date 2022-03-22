import json
from time import time
from fastapi.requests import Request
import logging

from main import logger


async def api_logger(request: Request, response):
    processed_time = time() - request.state.start
    status_code = response.status_code
    user = request.state.user

    log_data = dict(
        url=request.url.hostname + request.url.path,
        method=str(request.method),
        status_code=status_code,
        client=dict(
            ip=request.state.ip,
            user=user
        ),
        processed_time=str(round(processed_time * 1000, 5)) + "ms"
    )

    # HTTP Status Code 가 500번대 이상일 경우
    if response.status_code >= 500:
        logger.error(json.dumps(log_data))
    # API 1초를 초과한 경우
    elif processed_time > 1:
        logger.warn(json.dumps(log_data))
    # 정상적인 동작
    else:
        logger.info(json.dumps(log_data))


class DatabaseHandler(logging.Handler):
    def emit(self, record):
        self.format(record)

        import json
        from conf.databases import LogSession
        from apps.backend.graphql.logger.models import Log
        url = json.loads(record.message).get('url') \
            if record.message and str(record.message).strip() != '' else None
        db = LogSession()
        log = Log(
            log_level=record.levelname, message=record.message, url=url
        )
        db.add(log)
        db.commit()
        db.close()
