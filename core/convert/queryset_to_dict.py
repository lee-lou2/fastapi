from typing import List


def queryset_to_dict(model, *args, exclude: List = None) -> dict:
    """
    데이터베이스 쿼리를 딕셔너리로 변환
    :param model:
    :param args:
    :param exclude:
    :return:
    """
    q_dict = {}
    for c in model.__table__.columns:
        if not args or c.name in args:
            if not exclude or c.name not in exclude:
                q_dict[c.name] = getattr(model, c.name)

    return q_dict
