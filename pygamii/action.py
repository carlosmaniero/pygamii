# coding: utf-8
from __future__ import unicode_literals
import threading
import readchar
import time


class Action(threading.Thread):
    interval = 0
    running = False
    paused = False

    def __init__(self, scene, *args, **kwargs):
        self.scene = scene
        super(Action, self).__init__(*args, **kwargs)

    def run(self):
        while self.running:
            if not self.paused:
                self.do()
            if self.interval:
                time.sleep(self.interval)

    def stop(self):
        self.running = False
        self.paused = False

    def pause(self):
        self.paused = True

    def start(self, *args, **kwargs):
        self.running = True
        if self.paused:
            self.paused = False
        else:
            super(Action, self).start(*args, **kwargs)

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


class MultipleMoveAction(Action):
    def do(self):
        objects = self.scene.objects
        total_objects = len(objects)

        for obj1 in objects:
            if obj1.is_kill:
                self.scene.remove_object(obj1)
                total_objects -= 1
            else:
                if obj1.in_move():
                    obj1.move()
                    obj1.last_move = time.time()
                    for obj2 in objects:
                        if obj1 is not obj2 and obj1.colision(obj2):
                            obj1.on_colision(obj2)
                            obj2.on_colision(obj1)
