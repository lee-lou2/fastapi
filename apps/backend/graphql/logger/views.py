import strawberry
from strawberry.asgi import GraphQL
from typing import List

from apps.backend.graphql.logger.models import Log
from apps.backend.graphql.logger.schemas import LogSchema


def get_logs(
        created: str = None,
        url: str = None,
        log_level: str = None,
        message: str = None
):
    qs = {}
    if created:
        qs['created'] = created
    if url:
        qs['url'] = url
    if log_level:
        qs['log_level'] = log_level
    if message:
        qs['message'] = message
    from conf.databases import LogSession

    db = LogSession()
    return db.query(Log).filter_by(**qs)


@strawberry.type
class Query:
    all_logs: List[LogSchema] = strawberry.field(resolver=get_logs)


schema = strawberry.Schema(
    query=Query
)
graphql_app = GraphQL(schema)
