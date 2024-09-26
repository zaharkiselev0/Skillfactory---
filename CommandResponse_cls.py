from enum import Enum, unique


@unique
class ResponseType(Enum):
    HIT_MISS = 0
    HIT_GOT = 1
    HIT_KILL = 2
    SCOUT = 3


class CommandResponse:
    def __init__(self, resp_type: ResponseType):
        self.response_type = resp_type


class HitResponse(CommandResponse):
    def __init__(self, resp_type: ResponseType, x: int, y: int):
        super().__init__(resp_type)
        self.x = x
        self.y = y


class ScoutResponse(CommandResponse):
    def __init__(self, resp_type: ResponseType, ship_points: list[list[int]],
                 cords: list[list[int]], scout_points: list[bool]):
        super().__init__(resp_type)
        self.ship_points = ship_points
        self.cords_to_scout = cords
        self.scout_points = scout_points
