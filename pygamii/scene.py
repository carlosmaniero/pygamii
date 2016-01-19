# coding: utf-8
from __future__ import unicode_literals
from pygamii.utils import get_color_pair
import time
import platform
import os
import curses

# hack to use 256 colors
os.environ["TERM"] = "xterm-256color"

stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)
curses.flushinp()
curses.cbreak()
curses.curs_set(0)
current_os = platform.system()


class BaseScene(object):
    # prints per seconds
    pps = 1200
    rows = 23
    cols = 80
    blank_char = ' '
    char = ' '
    color = 'white'
    bg_color = 'black'
    playing = False
    objects = []
    actions = []

    def __init__(self, **kwargs):
        self.objects = []
        self.actions = []
        self.pair = get_color_pair(self.color, self.bg_color)

        for key, value in kwargs.items():
            if key not in ('objects', 'actions') and hasattr(self, key):
                setattr(self, key, value)
            else:
                raise Exception('Key "{}" not found'.format(key))

    def change_color(self, color, bg_color=None):
        self.color = color
        if self.bg_color:
            self.bg_color = self.bg_color
        self.pair = get_color_pair(self.color, self.bg_color)

    def add_object(self, obj):
        obj.scene = self
        obj.on_create()
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)
        obj.on_destroy()
        del obj

    def add_action(self, action, auto_start=True):
        action.scene = self
        action.on_create()
        self.actions.append(action)

        if auto_start:
            action.start()

    def remove_action(self, action):
        self.actions.remove(action)
        action.on_destroy()

    def clean(self):
        stdscr.clear()

    def get_terminal_size(self):
        x, y = stdscr.getmaxyx()
        x, y = y, x
        return x, y

    def render(self):
        for i in range(self.rows):
            stdscr.addstr(i, 0, ' ' * self.cols, self.pair)

        for obj in self.objects:
            lines = str(obj).split('\n')
            for i, text in enumerate(lines):
                y = obj.y + i
                for j, char in enumerate(text):
                    x = obj.x + j

                    if x >= 0 and y >= 0 and x <= self.cols and y <= self.rows:
                        bg_none = obj.get_bg_color(j, i) is None

                        if char != ' ' or not bg_none:
                            color = obj.get_color(j, i) or self.color
                            bg_color = obj.get_bg_color(j, i) or self.bg_color

                            pair = get_color_pair(color, bg_color)

                            stdscr.addstr(y, x, char, pair)

        stdscr.addstr(self.rows, 0, ' ' * (self.cols - 1))
        stdscr.refresh()

    def start(self):
        if current_os == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
        first = True
        self.playing = True
        while self.playing:
            if not first:
                time.sleep(0.05)
            else:
                first = False
            if self.playing:
                self.render()

    def stop(self):
        self.playing = False

        actions = self.actions[:]
        for action in actions:
            action.stop()
            self.remove_action(action)

        objects = self.objects[:]
        for obj in objects:
            self.remove_object(obj)

        stdscr.erase()
