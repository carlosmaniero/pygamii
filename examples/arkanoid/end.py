# coding: utf-8
from __future__ import unicode_literals
from pygamii.scene import BaseScene
from pygamii.objects import Object
from pygamii.action import MoveAction
from pygamii.audio import Audio


class Logo(Object):
    width = 80
    height = 5
    speed = 9
    y = 24
    _moving = True
    color = 'red'

    def __str__(self):
        return "                           ______        __           \n                             / /        /  `         /\n                          --/ /_  _    /--  ____  __/ \n                         (_/ / /_</_  (___,/ / <_(_/_ \n                                                      "

    def move(self):
        self.y -= 1

        if self.y <= -6:
            self.scene.stop()


class Scene(BaseScene):
    def __init__(self, **kwargs):
        super(Scene, self).__init__(**kwargs)
        self.music = Audio('songs/infected_powerball.ogg')
        self.music.play()

        logo = Logo()
        self.add_object(logo)
        self.add_action(MoveAction(logo))

    def stop(self):
        super(Scene, self).stop()
        self.music.stop()
