from fastapi import APIRouter, Request

from core.templates import template

router_v1 = APIRouter()


@router_v1.get("/")
async def client(request: Request):
    return template.init.TemplateResponse("client.html", {"request": request})
