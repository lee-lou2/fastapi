from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from apps.backend.external.cafe24.schemas import CreateProductRequestBase
from conf.databases import get_db
from apps.backend.external.cafe24.models import *

# 라우터
router_v1 = APIRouter()


@router_v1.post("/", status_code=201)
async def create_product(
        *,
        request: Request,
        db: Session = Depends(get_db),
        obj_in: CreateProductRequestBase
):
    return {'is_create': obj_in.save()}
