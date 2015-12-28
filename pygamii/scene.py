# coding: utf-8
from __future__ import unicode_literals
import os
import time
from termcolor import colored


class BaseScene(object):
    # prints per seconds
    pps = 1200
    rows = 23
    cols = 80
    blank_char = ' '
    char = ' '
    color = None
    bg_color = None
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
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_terminal_size(self):
        # TODO: compatibility
        row, col = os.popen('stty size', 'r').read().split()
        row = int(row)
        col = int(col)
        return row, col

    def render(self):
        screen_len = self.rows * self.cols
        if self.color or self.bg_color:
            screen = [colored(self.char, self.color, self.bg_color)] * screen_len
        else:
            screen = [self.char] * screen_len

        total_rows, total_cols = self.get_terminal_size()

        for obj in self.objects:
            lines = str(obj).split('\n')
            for i, text in enumerate(lines):
                y = obj.y + i
                for j, char in enumerate(text):
                    x = obj.x + j

                    if obj.color:
                        char = colored(char, obj.color, obj.bg_color)

                    position = self.cols * y + x
                    if position >= 0 and position < screen_len:
                        screen[position] = char

        to_print = ''
        for i, char in enumerate(screen, start=1):
            to_print += char
            if i % self.cols == 0 and total_cols > self.cols:
                to_print += self.blank_char * (total_cols - self.cols)
        self.clean()
        print(to_print)

    def start(self):
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

        #self.clean()
