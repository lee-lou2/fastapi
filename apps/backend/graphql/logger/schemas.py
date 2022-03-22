import strawberry


@strawberry.type
class LogSchema:
    created: str
    url: str
    log_level: str
    message: str
