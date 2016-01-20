from pygamii.objects import Object, ToRenderMixin
from pygamii.action import MultipleMoveAction, BaseKeyboard
from pygamii.audio import Audio
from pygamii.scene import BaseScene
import time
from enemies import EnemyGenerator
from score import Score
from player import Airplane
import os


class Debug(Object):
    def __str__(self):
        return str(len(self.scene.objects))


class Keyboard(BaseKeyboard):
    def handler(self, key):
        if key == ord(' '):
            self.scene.stop()
        elif key == ord('q'):
            os._exit(0)


class Logo(ToRenderMixin, Object):
    to_render = '\n'.join([
        '·▄▄▄▄▄▌   ▄· ▄▌ ▄▄·       • ▌ ▄ ·. ▄▄▄▄·  ▄▄▄· ▄▄▄▄▄',
        '▐▄▄·██•  ▐█▪██▌▐█ ▌▪▪     ·██ ▐███▪▐█ ▀█▪▐█ ▀█ •██  ',
        '██▪ ██▪  ▐█▌▐█▪██ ▄▄ ▄█▀▄ ▐█ ▌▐▌▐█·▐█▀▀█▄▄█▀▀█  ▐█.▪',
        '██▌.▐█▌▐▌ ▐█▀·.▐███▌▐█▌.▐▌██ ██▌▐█▌██▄▪▐█▐█ ▪▐▌ ▐█▌·',
        '▀▀▀ .▀▀▀   ▀ • ·▀▀▀  ▀█▄▀▪▀▀  █▪▀▀▀·▀▀▀▀  ▀  ▀  ▀▀▀ ',
        '                                                    ',
        '              Press space to start                  '
    ])

    width = 55
    height = 6
    _moving = True
    red = True
    speed = 50
    y = -6
    color = 'green'
    enemy_started = False

    def on_create(self):
        self.music = Audio('songs/intro.ogg')
        self.music.play(True)
        self.scene.bg_color = 'blue'
        self.scene.change_color(self.color, self.bg_color)

    def on_destroy(self):
        self.music.stop()

    def move(self):
        self.scene.objects.remove(self)
        self.scene.objects.append(self)
        self.x = int(self.scene.cols / 2) - int(self.width / 2)
        y = int(self.scene.rows / 2) - int(self.height / 2)

        if self.y != y:
            self.y += 1
        else:
            if not self.enemy_started:
                self.scene.add_action(EnemyGenerator())
                self.enemy_started = True
            self.speed = 4
            if self.color == 'red':
                self.color = 'green'
            elif self.color == 'green':
                self.color = 'white'
            else:
                self.color = 'red'


class PyGamii(ToRenderMixin, Object):
    print_list = [
        '██████╗ ██╗   ██╗ ██████╗  █████╗ ███╗   ███╗██╗██╗',
        '██╔══██╗╚██╗ ██╔╝██╔════╝ ██╔══██╗████╗ ████║╚═╝╚═╝',
        '██████╔╝ ╚████╔╝ ██║  ███╗███████║██╔████╔██║██╗██╗',
        '██╔═══╝   ╚██╔╝  ██║   ██║██╔══██║██║╚██╔╝██║██║██║',
        '██║        ██║   ╚██████╔╝██║  ██║██║ ╚═╝ ██║█╔╝█╔╝',
        '╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚╝ ╚╝ ',
    ]
    to_render = '\n'.join(print_list)
    width = 51
    height = 6
    color = 'blue'
    _moving = True
    y = -6
    speed = 20
    blink = 2
    cleaned = 0
    wait = 0.25
    started = None
    bg_music = Audio('songs/pygamii-bg.ogg')

    def on_create(self):
        music = Audio('songs/pygamii-open.ogg')
        music.play()
        self.started = time.time()
        self.bg_music.play(True)

    def on_destroy(self):
        self.bg_music.stop()

    def move(self):
        if time.time() - self.started < self.wait:
            return
        self.x = int(self.scene.cols / 2) - int(self.width / 2)
        y = int(self.scene.rows / 2) - int(self.height / 2)

        if y != self.y:
            self.y += 1
        elif self.blink:
            if self.blink == 2:
                music = Audio('songs/pygamii-blink.ogg')
                music.play()

            self.speed = 5
            if self.color == 'blue':
                self.color = 'yellow'
            else:
                self.color = 'blue'
            self.blink -= 1
            if self.blink == 0:
                self.wait = 2
                self.started = time.time()
        elif self.scene.presents.centered:
            Audio('songs/pygamii-out.ogg').play()
            self.print_list[self.cleaned] = ''
            self.to_render = '\n'.join(self.print_list)
            if self.cleaned < len(self.print_list) - 1:
                self.cleaned += 1
            else:
                self.scene.presents.is_kill = True
                self.is_kill = True
                self.scene.add_object(Logo())


class Presents(ToRenderMixin, Object):
    to_render = 'Presents'
    width = len(to_render)
    height = 1
    _moving = True
    speed = 150
    x = -10
    centered = False

    def move(self):
        logo = self.scene.pygamii
        self.y = logo.y + logo.height + 1
        x = int(self.scene.cols / 2) - int(self.width / 2)

        if logo.blink == 0:
            if self.x != x:
                self.x += 1
            else:
                self.centered = True


class Scene(BaseScene):
    def __init__(self, *args, **kwargs):
        super(Scene, self).__init__(*args, **kwargs)
        self.cols, self.rows = self.get_terminal_size()
        self.rows -= 1
        self.add_action(MultipleMoveAction())
        self.pygamii = PyGamii()
        self.presents = Presents()

        self.add_object(self.pygamii)
        self.add_object(self.presents)

        self.airplane = Airplane(self)
        self.score = Score()
        self.add_object(Debug())

        self.add_action(Keyboard())
