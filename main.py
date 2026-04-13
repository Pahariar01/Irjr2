from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from simulation import engine
from ws_manager import manager
import asyncio

app = FastAPI()

@app.on_event("startup")
async def start():
    asyncio.create_task(engine.run())

@app.get("/")
def home():
    return {"status": "IRJR running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "control":
                t_id = data["train_id"]
                if t_id in engine.trains:
                    engine.trains[t_id].throttle = float(data["throttle"])
    except WebSocketDisconnect:
        manager.disconnect(websocket)