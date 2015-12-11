# coding: utf-8
from __future__ import unicode_literals


class Object:
    width = 1
    height = 1
    x = 0
    y = 0
    color = None
    char = 'x'
    scene = None
    speed = 1
    _moving = False

    def get_char(self):
        return self.char

    def __str__(self):
        return (self.get_char() * self.width + '\n') * self.height

    def colision(self, obj):
        return (
            self.y >= obj.y and self.y <= obj.y + obj.height and
            self.x >= obj.x and self.x <= obj.x + obj.width
        )

    def on_colision(self, obj):
        pass

    def in_move(self):
        return self._moving

    def move(self):
        raise NotImplementedError

    @property
    def cords(self):
        return (self.x, self.y, self.width, self.height)
