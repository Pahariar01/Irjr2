from pydantic import BaseModel

class Train(BaseModel):
    id: str
    name: str
    position: float = 0
    speed: float = 0
    throttle: float = 0
    max_speed: float = 33.3
    is_player_controlled: bool = False
    next_station_dist: float = 5000
    status: str = "running"