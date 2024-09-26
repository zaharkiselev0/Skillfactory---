#from abc import ABCMeta,  abstractmethod
from collections.abc import Iterable
from Point_cls import *
from Errors import *
from CommandResponse_cls import *


class Ship:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        if start.x != end.x and start.y != end.y:
            raise ShipCreateError("Корабль должен находиться на одной линии")
        self.health = 1 + abs(start.x - end.x) + abs(start.y - end.y)

    def points(self) -> Iterable[Point]:
        if self.start.x == self.end.x:
            for j in range(self.start.y, self.end.y + 1):
                yield Point(self.start.x, j)
        else:
            for i in range(self.start.x, self.end.x + 1):
                yield Point(i, self.start.y)

    def getHit(self, p: Point) -> HitResponse:
        self.health -= 1
        if self.health:
            return HitResponse(ResponseType.HIT_GOT, p.x, p.y)
        else:
            return HitResponse(ResponseType.HIT_KILL, p.x, p.y)


