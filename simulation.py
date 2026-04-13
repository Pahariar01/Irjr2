import asyncio
from models import Train
from ws_manager import manager

class Engine:
    def __init__(self):
        self.trains = {
            "T1": Train(id="T1", name="Rajdhani", next_station_dist=2000),
            "T2": Train(id="T2", name="Vande Bharat", next_station_dist=5000),
        }
        self.tick = 0.5

    async def run(self):
        while True:
            for t in self.trains.values():
                if not t.is_player_controlled:
                    t.throttle = 0.5

                t.speed += t.throttle * 0.5
                t.speed = max(0, min(t.speed, t.max_speed))
                t.position += t.speed * self.tick

            await manager.broadcast({
                "type": "update",
                "trains": [t.dict() for t in self.trains.values()]
            })

            await asyncio.sleep(self.tick)

engine = Engine()