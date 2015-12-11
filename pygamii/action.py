# coding: utf-8
from __future__ import unicode_literals
import threading
import readchar
import time


class Action(threading.Thread):
    interval = 0
    running = False

    def __init__(self, scene, *args, **kwargs):
        self.scene = scene
        super(Action, self).__init__(*args, **kwargs)

    def start(self, *args, **kwargs):
        self.running = True
        super(Action, self).start()

    def run(self):
        while self.running:
            self.do()
            if self.interval:
                time.sleep(self.interval)

    def stop(self):
        self.running = False

    def do(self):
        raise NotImplemented


class BaseKeyboard(Action):
    def do(self):
        key = readchar.readchar()
        self.handler(key)

    def handler(self, key):
        raise NotImplementedError


class MoveAction(Action):
    def __init__(self, obj, scene, *args, **kwargs):
        self.obj = obj
        super(MoveAction, self).__init__(scene, *args, **kwargs)

    def do(self):
        if self.obj.in_move():
            self.interval = 1 / self.obj.speed
            self.obj.move()

            for obj in self.scene.objects:
                if obj is not self.obj and self.obj.colision(obj):
                    self.obj.on_colision(obj)
