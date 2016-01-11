# coding: utf-8
from __future__ import unicode_literals
from pygamii.scene import BaseScene
from pygamii.objects import Object
from pygamii.action import BaseKeyboard, MoveAction
from pygamii.audio import Audio

import os


class Keyboard(BaseKeyboard):
    def handler(self, key):
        if key == ord(' '):
            self.scene.stop()
        elif key == ord('q'):
            self.scene.clean()
            os._exit(0)


class Logo(Object):
    width = 80
    height = 7
    speed = 10
    y = 5
    colors = ['red', 'cyan', 'green', 'yellow']
    color = colors[0]
    color_index = 0
    _moving = True

    def __str__(self):
        return "                      _        _                     _     _ \n                     /_\  _ __| | ____ _ _ __   ___ (_) __| |\n                    //_\\\\| '__| |/ / _` | '_ \ / _ \| |/ _` |\n                   /  _  \ |  |   < (_| | | | | (_) | | (_| |\n                   \_/ \_/_|  |_|\_\__,_|_| |_|\___/|_|\__,_|\n                                                             "

    def move(self):
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.color = self.colors[self.color_index]


class HelpText(Object):
    width = 80
    height = 2
    y = 11

    def __str__(self):
        return '~Press SPACE to start or Q for quit.~'.center(80) + '\n' + 'Game Control: [a] [s] [d] [w]'.center(80)


class Scene(BaseScene):
    def __init__(self, **kwargs):
        super(Scene, self).__init__(**kwargs)
        self.music = Audio('songs/infected_powerball.ogg')
        self.music.play()

        logo = Logo()
        self.add_object(logo)
        self.add_action(MoveAction(logo))

        help = HelpText()
        self.add_object(help)

        self.add_action(Keyboard())

    def stop(self):
        super(Scene, self).stop()
        self.music.stop()
