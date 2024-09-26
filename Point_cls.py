from Errors import *
import random
#random.seed(1)


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f'({self.x},{self.y})'

    def __str__(self):
        return f'({self.x + 1},{self.y + 1})'
