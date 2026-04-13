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
@app.post("/control")
async def control_train(data: dict):
    train_id = data.get("train_id")
    throttle = float(data.get("throttle", 0))

    if train_id in engine.trains:
        train = engine.trains[train_id]
        if train.is_player_controlled:
            train.throttle = max(-1.0, min(1.0, throttle))
            return {"status": "ok", "throttle": train.throttle}

    return {"status": "error"}
@app.get("/trains")
def get_trains():
    return engine.trains
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message: {data}")
