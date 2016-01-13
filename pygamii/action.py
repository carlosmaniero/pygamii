# coding: utf-8
from __future__ import unicode_literals
import threading
import time
import curses


class Action(threading.Thread):
    interval = 0.01
    running = False
    paused = False

    def __init__(self, *args, **kwargs):
        super(Action, self).__init__(*args, **kwargs)

    def run(self):
        try:
            while self.running:
                if not self.paused:
                    self.do()
                if self.interval:
                    time.sleep(self.interval)
        except Exception as e:
            print(e)
            import os
            os._exit(0)

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

    def on_create(self):
        pass

    def on_destroy(self):
        pass


class BaseKeyboard(Action):
    def do(self):
        key = self.stdscr.getch()
        self.handler(key)

    def handler(self, key):
        raise NotImplementedError

    def on_create(self):
        # To handler getch and render, we need create a custom windows
        self.stdscr = curses.newwin(0, 0, 0, 0)
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)


class MoveAction(Action):
    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        super(MoveAction, self).__init__(*args, **kwargs)

    def do(self):
        if self.obj.in_move():
            self.interval = 1 / self.obj.speed
            self.obj.move()

            for obj in self.scene.objects:
                if obj is not self.obj and self.obj.collision(obj):
                    self.obj.on_collision(obj)


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
                        if obj1 is not obj2 and obj1.collision(obj2):
                            obj1.on_collision(obj2)
                            obj2.on_collision(obj1)


class EventAction(Action):
    _events = {}
    triggeds = []

    def register(self, event, fn):
        self._events.setdefault(event, [])
        self._events[event].append(fn)

    def trigger(self, event, *args, **kwargs):
        self.triggeds.append((event, args, kwargs))

    def do(self):
        triggeds = self.triggeds[:]
        for trigger in triggeds:
            event, args, kwargs = trigger
            events = self._events.get(event, [])

            for event in events:
                event(*args, **kwargs)

            self.triggeds.remove(trigger)
