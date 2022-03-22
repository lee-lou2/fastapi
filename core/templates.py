from starlette.templating import Jinja2Templates

from conf.settings.prod import settings


class BaseTemplate:
    """
    템플릿 생성
    """
    def __init__(self):
        self.directory = f"{settings.BASE_PATH}/templates"

    @property
    def init(self):
        return Jinja2Templates(directory=self.directory)


template = BaseTemplate()
