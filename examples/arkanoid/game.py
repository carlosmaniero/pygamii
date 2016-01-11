# coding: utf-8
from __future__ import unicode_literals
from pygamii.scene import BaseScene
from pygamii.objects import Object
from pygamii.action import BaseKeyboard, MoveAction
from pygamii.audio import Audio


class Keyboard(BaseKeyboard):
    def __init__(self, cursor, ball, *args, **kwargs):
        self.cursor = cursor
        self.ball = ball
        super(Keyboard, self).__init__(*args, **kwargs)

    def handler(self, key):
        if key == ord('a'):
            if self.cursor.x > 0:
                self.cursor.x -= 1
                if not self.ball.started:
                    self.ball.x -= 1
        elif key == ord('d'):
            if self.cursor.x + self.cursor.width <= self.scene.cols - 1:
                self.cursor.x += 1
                if not self.ball.started:
                    self.ball.x += 1
        elif key == ord(' '):
            self.ball.started = True
        elif key == ord('q'):
            self.scene.stop()


class Cursor(Object):
    y = 22
    width = 7
    height = 1
    color = 'blue'


class Block(Object):
    width = 5
    char = '='
    resistence = 3

    def dec_resistence(self):
        self.set_resistence(self.resistence - 1)

    def set_resistence(self, value):
        self.resistence = value
        if self.resistence == 3:
            self.char = '='
            self.color = 'red'
        elif self.resistence == 2:
            self.char = '='
            self.color = 'yellow'
        elif self.resistence == 1:
            self.char = '='
            self.color = 'green'


class Ball(Object):
    color = 'cyan'
    y = 21
    x = 3
    char = 'o'
    started = False
    move_x = 1
    move_y = -1
    speed = 15.0
    lives = 3
    song_collision = None

    def __init__(self, *args, **kwargs):
        self.song_collision = Audio('songs/pipe9.ogg')
        self.song_lose = Audio('songs/lose.ogg')

    def set_cursor(self, cursor):
        self.cursor = cursor

    def in_move(self):
        return self.started

    def move(self):
        self.x += self.move_x
        self.y += self.move_y

        if self.y < 0:
            self.song_collision.play()
            self.y = 1
            self.move_y = 1

        if self.x >= self.scene.cols:
            self.song_collision.play()
            self.x = self.scene.cols - 1
            self.move_x = -1

        if self.x < 0:
            self.song_collision.play()
            self.x = 0
            self.move_x = 1

        if self.y >= 23:
            self.song_lose.play()
            self.lives -= 1
            if self.lives:
                self.x = self.cursor.x + int(self.cursor.width / 2)
                self.started = False
                self.y = 21
                self.move_y = -1
            else:
                self.scene.stop()

    def on_collision(self, obj):
        self.song_collision.play()
        if isinstance(obj, Cursor):
            self.move_y = -1
            self.y -= 2
        elif isinstance(obj, Block):
            self.move_y *= -1
            obj.dec_resistence()
            if obj.resistence == 0:
                self.scene.objects.remove(obj)


class Scene(BaseScene):
    music = None

    def __init__(self, **kwargs):
        super(Scene, self).__init__(**kwargs)

        cursor = Cursor()

        self.music = Audio('songs/infected_powerball.ogg')
        self.music.play(True)

        ball = Ball()
        ball.set_cursor(cursor)

        self.add_action(Keyboard(cursor, ball))
        self.add_action(MoveAction(ball))

        self.add_object(cursor)
        self.add_object(ball)

        for i in range(0, int(80 / 5)):
            block = Block()
            block.set_resistence(3)
            block.x = 5 * i
            self.add_object(block)

        for i in range(0, int(80 / 5)):
            block = Block()
            block.set_resistence(2)
            block.x = 5 * i
            block.y = 1
            self.add_object(block)

        for i in range(0, int(80 / 5)):
            block = Block()
            block.set_resistence(1)
            block.x = 5 * i
            block.y = 2
            self.add_object(block)

    def stop(self):
        super(Scene, self).stop()
        self.music.stop()
