# coding: utf-8
from __future__ import unicode_literals
from pygamii.utils import get_terminal_size, init_colors, get_color_pair
import time
import platform
import os
import curses

stdscr = curses.initscr()
curses.start_color()
current_os = platform.system()

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
init_colors()


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

        for key, value in kwargs.items():
            if key not in ('objects', 'actions') and hasattr(self, key):
                setattr(self, key, value)
            else:
                raise Exception('Key "{}" not found'.format(key))

    def add_object(self, obj):
        obj.scene = self
        self.objects.append(obj)
        obj.on_create()

    def remove_object(self, obj):
        self.objects.remove(obj)
        obj.on_destroy()

    def add_action(self, action_class, *args, **kwargs):
        auto_start = True
        if kwargs.get('_auto_start') is not None:
            auto_start = kwargs.pop('_auto_start')

        kwargs['scene'] = self
        action = action_class(*args, **kwargs)
        self.actions.append(action)

        action.on_create()

        if auto_start:
            action.start()

    def remove_action(self, action):
        self.actions.remove(action)
        action.on_destroy()

    def clean(self):
        total_cols, total_rows = self.get_terminal_size()
        print(' ' * total_cols * (total_rows - 1))

    def get_terminal_size(self):
        return get_terminal_size()

    def render(self):
        screen_len = self.rows * self.cols

        for i in range(self.rows):
            stdscr.addstr(i, 0, ' ' * self.cols)

        for obj in self.objects:
            lines = str(obj).split('\n')
            for i, text in enumerate(lines):
                y = obj.y + i
                for j, char in enumerate(text):
                    x = obj.x + j

                    color = obj.color or self.color
                    bg_color = obj.bg_color or self.bg_color

                    pair = get_color_pair(color, bg_color)

                    position = self.cols * y + x
                    if position >= 0 and position < screen_len:
                        if char != ' ' or self.bg_color is not None:
                            stdscr.addstr(y, x, char, pair)

        stdscr.addstr(self.rows, 0, ' ')
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

        for action in self.actions:
            action.stop()

