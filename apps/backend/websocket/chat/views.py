from fastapi import APIRouter, WebSocket

# 라우터
router_v1 = APIRouter()


@router_v1.websocket("/backend")
async def websocket_endpoint(websocket: WebSocket):
    print(f"client connected : {websocket.client}")
    await websocket.accept()
    await websocket.send_text(f"Welcome client : {websocket.client}")
    while True:
        data = await websocket.receive_text()
        print(f"message received : {data} from : {websocket.client}")
        await websocket.send_text(f"Message text was: {data}")
