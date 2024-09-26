from Grid_cls import *
from collections import OrderedDict
import random


class Player:
    def __init__(self, row_num, col_num):
        self.grid = Grid(row_num, col_num)
        allowed_hits = [Point(i, j) for i in range(row_num) for j in range(col_num)]
        random.shuffle(allowed_hits)
        self.hits = OrderedDict(dict.fromkeys(allowed_hits, None))

    def hit(self, player, point: Point) -> HitResponse:
        if not player.grid.checkPoint(point):
            raise HitError(f"Клетка {point} находится за пределами поля")
        if point not in self.hits:
            raise HitError(f"Вы уже стреляли в клетку {point}")  # другой тип ошии? & добавить провку на выход за пре

        self.hits.pop(point)
        return player.getHit(point)

    def getHit(self, point):
        return self.grid.getHit(point)

    def add(self, ship: Ship):
        return self.grid.add(ship)

    def scout(self, player, row_num: int, vertical: bool = True) -> ScoutResponse:
        if vertical and not 0 <= row_num <= self.grid.col_num or not vertical and not 0 <= row_num <= self.grid.row_num:
            raise ScoutError("Номер строки(столбца) за пределами поля")
        ship = random.choice(self.grid.ships)
        self.grid.ships.remove(ship)
        ship_points = [[p.x, p.y] for p in ship.points()]
        if vertical:
            line = [Point(i, row_num) for i in range(self.grid.row_num)]
        else:
            line = [Point(row_num, i) for i in range(self.grid.col_num)]

        coords = [[p.x - 1, p.y - 1] for p in line]
        scout_points = list(map(self.grid.point_to_ship.__contains__, line))
        return ScoutResponse(ResponseType.SCOUT, ship_points, coords, scout_points)



