from math import sqrt
from random import randint

from pygame import Surface, Rect
from pygame.draw import rect


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class CrazyPlane:
    def __init__(self, x=0, y=0) -> None:
        self.__pos = Position(x, y)
        self.__turn_count = 0

    def update(self):
        self.__pos.x += randint(-1, 1)
        self.__pos.x = abs(self.__pos.x) % 10

        self.__pos.y += randint(-1, 1)
        self.__pos.y = abs(self.__pos.y) % 10

    def __str__(self) -> str:
        return f"Plane is at ({self.__pos.x}, {self.__pos.y})"

    def turn(self, other: "CrazyPlane") -> None:
        self.__pos.x += self.__pos.x - other.__pos.x
        self.__pos.x = abs(self.__pos.x) % 10

        self.__pos.y += self.__pos.y - other.__pos.y
        self.__pos.y = abs(self.__pos.y) % 10

        self.__turn_count += 1

    def should_destroy(self) -> bool:
        return self.__turn_count > 2

    def distance(self, other: "CrazyPlane"):
        return sqrt(
            (self.__pos.x - other.__pos.x) ** 2 + (self.__pos.y - other.__pos.y) ** 2
        )

    def get_position(self):
        return self.__pos

    def draw(self, surf: Surface, color=(177, 240, 238)):
        width: int = surf.get_width()
        height = surf.get_height()
        plane_pos = self.get_position()
        rect(
            surf,
            color,
            Rect(
                plane_pos.x * width // 10,
                plane_pos.y * height // 10,
                width // 10,
                height // 10,
            ),
        )

    def erase(self, surf: Surface):
        self.draw(surf, (0, 0, 0))
