# coding: utf-8
from __future__ import unicode_literals
import time


class Object(object):
    is_kill = False
    width = 1
    height = 1
    x = 0
    y = 0
    color = None
    bg_color = None
    char = 'x'
    scene = None
    speed = 1
    _moving = False
    last_move = 0

    def get_char(self):
        return self.char

    def __str__(self):
        return (self.get_char() * self.width + '\n') * self.height

    def collision(self, obj):
        return (
            self.x < obj.x + obj.width and self.x + self.width > obj.x and
            self.y < obj.y + obj.height and self.y + self.height > obj.y
        )

    def on_collision(self, obj):
        pass

    def in_move(self):
        if self.speed:
            return self._moving and time.time() - self.last_move > 1.0 / self.speed
        return self._moving

    def move(self):
        pass

    @property
    def cords(self):
        return (self.x, self.y, self.width, self.height)

    def on_create(self):
        pass

    def on_destroy(self):
        pass

    def get_color(self, col, row):
        return self.color

    def get_bg_color(self, col, row):
        return self.bg_color


class ToRenderMixin(object):
    to_render = '*'

    def __str__(self):
        return self.to_render
