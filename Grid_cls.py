from collections.abc import Iterable
from Ship_cls import *


class Grid:
    def __init__(self, row_num, col_num):
        self.ships = []
        self.point_to_ship = dict()
        self.row_num = row_num
        self.col_num = col_num

    def add(self, ship):
        self.shipCheck(ship)
        self.ships.append(ship)
        self.point_to_ship.update(dict.fromkeys(ship.points(), ship))

    def shipCheck(self, ship: Ship):
        if not self.checkPoint(ship.start) or not self.checkPoint(ship.end):
            raise ShipAddError("Координаты корабля выходят за пределы поля")

        for p in ship.points():
            for nearby_p in [p, p + Point(0, 1), p + Point(1, 0), p - Point(0, 1), p - Point(1, 0)]:
                if self.point_to_ship.get(nearby_p, ship) != ship:
                    raise ShipAddError("Корабли должны быть на расстоянии как минимум одной клетки друг от друга")
        return True

    def getHit(self, p: Point) -> HitResponse:
        if not self.checkPoint(p):
            raise HitError("Невозможно выстрелить в клетку вне поля")
        if ship := self.point_to_ship.get(p):
            hit_resp = ship.getHit(p)
            if hit_resp.response_type == ResponseType.HIT_KILL:
                self.ships.remove(ship)
            return hit_resp

        return HitResponse(ResponseType.HIT_MISS, p.x, p.y)

    def checkPoint(self, p: Point) -> bool:
        return 0 <= p.x < self.row_num and 0 <= p.y < self.col_num
