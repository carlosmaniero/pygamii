from pygamii.objects import Object
from pygamii.action import BaseKeyboard
from pygamii.audio import Audio
from weapon import BasicWeapon
import settings


class Airplane(Object):
    height = 5
    width = 11
    color = 'green'
    lives = 3
    kill_animation = False
    kill_steps = 5
    kill_music = Audio('songs/lose.ogg')
    to_render = ''
    _moving = True
    speed = 5

    def __init__(self, scene):
        self.weapon = BasicWeapon(scene, self)
        self.y = scene.rows - self.height
        self.x = int((scene.cols - self.width) / 2)
        self.to_render = '\n'.join([
            ' ▄   █   ▄ ',
            '███████████',
            ' ▀   █   ▀ ',
            '     █     ',
            '   ▀▀▀▀▀   ',
        ])

    def __str__(self):
        return self.to_render

    def up(self):
        if self.y > 0:
            self.y -= 1

    def down(self):
        if self.y < self.scene.rows - self.height:
            self.y += 1

    def is_live(self):
        return not self.kill_animation and self.lives > 0

    def left(self):
        if self.x > 6:
            self.x -= 1

    def right(self):
        if self.x < self.scene.cols - self.width - 6:
            self.x += 1

    def kill(self):
        if not self.kill_animation:
            self.kill_steps = 5
            self.kill_animation = True
            self.lives -= 1
            self.kill_music.play()

            if self.lives <= 0:
                self.scene.stop()

    def move(self):
        if self.kill_animation:
            if self.kill_steps % 2:
                self.color = 'red'
            else:
                self.color = 'white'
            self.kill_steps -= 1
            if self.kill_steps == 0:
                self.color = 'green'
                self.kill_animation = False


class Keyboard(BaseKeyboard):
    def handler(self, key):
        if key == settings.KEY_UP:
            self.scene.airplane.up()
        elif key == settings.KEY_DOWN:
            self.scene.airplane.down()
        elif key == settings.KEY_LEFT:
            self.scene.airplane.left()
        elif key == settings.KEY_RIGHT:
            self.scene.airplane.right()
        elif key == ord(' '):
            if self.scene.airplane.weapon:
                self.scene.airplane.weapon.shot()
        elif key == ord('m'):
            self.scene.music.stop()
        elif key == ord('p'):
            self.scene.music.play()
        elif key == ord('q'):
            self.scene.stop()
