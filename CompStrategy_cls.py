import random
from Player_cls import *
from abc import ABCMeta, abstractmethod


class CompStrategy(metaclass=ABCMeta):
    @abstractmethod
    def move(self, comp: Player, player: Player) -> CommandResponse:
        pass


class RandomHitStrategy(CompStrategy):
    def move(self, comp: Player, player: Player) -> CommandResponse:
        point = next(iter(comp.hits.keys()))
        return comp.hit(player, point)


class RandomHitImproved(CompStrategy):
    def __init__(self):
        self.hit_stack = []
        self.point = None
        self.dir = None
        self.ort_dir = None

    def move(self, comp: Player, player: Player) -> CommandResponse:
        if self.dir:
            self.point += self.dir
            if self.point not in comp.hits:
                self.dir = Point(0, 0) - self.dir
                while self.point not in comp.hits:
                    self.point += self.dir
            resp = comp.hit(player, self.point)

            if resp.response_type == ResponseType.HIT_MISS:
                self.dir = Point(0, 0) - self.dir
                while self.point + self.dir not in comp.hits:
                    self.point += self.dir
            else:
                for x in [self.point + self.ort_dir, self.point - self.ort_dir]:
                    if x in comp.hits:
                        comp.hits.pop(x)
                if resp.response_type == ResponseType.HIT_KILL:
                    if (t := self.point + self.dir) in comp.hits:
                        comp.hits.pop(t)
                        self.dir = self.point = self.ort_dir = None
            return resp

        if self.hit_stack:
            p = self.hit_stack.pop()
            resp = comp.hit(player, p)
            if resp.response_type != ResponseType.HIT_MISS:
                self.dir = p - self.point
                self.ort_dir = Point(self.dir.y, self.dir.x)
                for x in [p + self.ort_dir, p - self.ort_dir, self.point - self.dir]:
                    if x in comp.hits:
                        comp.hits.pop(x)
                self.point = p
                self.hit_stack = []

            if resp.response_type == ResponseType.HIT_KILL:
                if (t := p + self.dir) in comp.hits:
                    comp.hits.pop(t)
                self.dir = self.point = self.ort_dir = None
            return resp

        else:
            p = next(iter(comp.hits.keys()))
            resp = comp.hit(player, p)
            if resp.response_type == ResponseType.HIT_KILL:
                for x in [p + Point(0, 1), p + Point(1, 0), p - Point(0, 1), p - Point(1, 0)]:
                    if x in comp.hits:
                        comp.hits.pop(x)

            if resp.response_type == ResponseType.HIT_GOT:
                self.point = p
                self.hit_stack = [x for x in [p + Point(0, 1), p + Point(1, 0), p - Point(0, 1), p - Point(1, 0)] if x in comp.hits]
                random.shuffle(self.hit_stack)
            return resp

