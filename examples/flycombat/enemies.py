from pygamii.objects import Object
from pygamii.action import Action
from pygamii.audio import Audio
from gifts import get_gift
import random


class Enemy(Object):
    is_kill = False
    kill_animation = False
    kill_steps = 5
    explosion_audio = Audio('songs/explosion.ogg')

    def __init__(self, *args, **kwargs):
        super(Enemy, self).__init__(*args, **kwargs)
        self.gift_class = get_gift()
        if self.gift_class:
            self.color = self.gift_class.color

    def kill(self):
        if not self.kill_animation:
            self.scene.score.points += 5
            self.explosion_audio.song.set_volume(0.25)
            self.explosion_audio.play()
            self.kill_animation = True
            self.speed = 10

    def is_live(self):
        return not self.is_kill and not self.kill_animation

    def move(self):
        if self.kill_animation:
            if self.kill_steps % 2:
                self.color = 'red'
            else:
                self.color = 'white'
            self.kill_steps -= 1
            if self.kill_steps == 0:
                self.is_kill = True
                if self.gift_class:
                    gift = self.gift_class()
                    gift.x = self.x
                    gift.y = self.y
                    self.scene.add_object(gift)
        else:
            self.y += 1

    def on_colision(self, obj):
        if self.scene.airplane is obj and obj.is_live():
            self.kill()
            obj.kill()


class SimpleAirplaneEnemy(Enemy):
    y = -2
    height = 4
    width = 5
    color = 'yellow'
    speed = 5
    _moving = True
    to_render = '\n'.join([
        ' ▄▄▄ ',
        '  █  ',
        '█████',
        '  ▀  ',
    ])

    def __str__(self):
        return self.to_render


class EnemyGenerator(Action):
    interval = 3

    def __init__(self, scene, *args, **kwargs):
        super(EnemyGenerator, self).__init__(scene, *args, **kwargs)

    def do(self):
        airplane = SimpleAirplaneEnemy()
        airplane.x = random.randrange(0, self.scene.cols - airplane.width)
        self.scene.add_object(airplane)

    def stop(self):
        super(EnemyGenerator, self).stop()
