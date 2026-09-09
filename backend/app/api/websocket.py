from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/ws/generate")
async def ws_generate(websocket: WebSocket):
    await websocket.accept()
    for progress in (10, 35, 65, 100):
        await websocket.send_json({"progress": progress})
    await websocket.close()
