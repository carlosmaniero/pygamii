from pygamii.objects import Object
from pygamii.audio import Audio
from pygamii.action import Action
from enemies import Enemy
import time


class Bullet(Object):
    char = '*'
    color = 'red'
    _moving = True
    speed = 20
    music = 'songs/simpleshot.ogg'
    direction = -1

    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(*args, **kwargs)
        music = Audio(self.music)
        music.set_volume(0.25)
        music.play()

    def move(self):
        self.y += self.direction
        if self.y < 0 or self.y > self.scene.rows:
            self.is_kill = True

    def on_colision(self, obj):
        if isinstance(obj, Bullet):
            self.is_kill = True
            obj.is_kill = True


class AirPlaneBullet(Bullet):
    def on_collision(self, obj):
        if isinstance(obj, Enemy) and obj.is_live():
            obj.kill()
            self.y = -1


class EnemyBullet(Bullet):
    direction = 1

    def on_collision(self, obj):
        super(EnemyBullet, self).on_colision(obj)
        if obj is self.scene.airplane:
            self.scene.airplane.kill()
            self.is_kill = True


class EnemyBoomb(EnemyBullet):
    width = 3
    height = 3
    to_render = '\n'.join([
        ' ▄ ',
        '███',
        ' ▀ ',
    ])

    def __str__(self):
        return self.to_render


class Weapon(object):
    bullet_class = AirPlaneBullet
    delay = 0.10
    last_shot = None

    def __init__(self, scene, airplane):
        self.scene = scene
        self.airplane = airplane

    def shot(self):
        pass

    def remove(self):
        self.airplane.weapon = None


class BasicWeapon(Weapon):
    def shot(self):
        current = time.time() - self.delay

        if self.last_shot is None or self.last_shot < current:
            bullet = self.bullet_class()
            bullet.x = self.airplane.x + int(self.airplane.width / 2)
            bullet.y = self.airplane.y
            self.scene.add_object(bullet)
            self.last_shot = time.time()


class MultipleWeaponAction(Action):
    interval = 0.10
    shots = 100

    def __init__(self, airplane, bullet_class, *args, **kwargs):
        super(MultipleWeaponAction, self).__init__(*args, **kwargs)
        self.bullet_class = bullet_class
        self.airplane = airplane

    def do(self):
        bullet = self.bullet_class()
        bullet.x = self.airplane.x + int(self.airplane.width / 2)
        bullet.y = self.airplane.y
        self.scene.add_object(bullet)
        self.last_shot = time.time()
        self.shots -= 1
        if self.shots == 0:
            self.stop()
            self.airplane.weapon = BasicWeapon(self.scene, self.airplane)
            self.scene.remove_action(self)


class MultipleWeapon(Weapon):
    def __init__(self, scene, airplane):
        super(MultipleWeapon, self).__init__(scene, airplane)
        self.action = MultipleWeaponAction(airplane, AirPlaneBullet)
        scene.add_action(self.action)

    def shot(self):
        if self.action.running and not self.action.paused:
            self.action.pause()
        else:
            self.action.start()

    def remove(self):
        self.action.stop()
        super(MultipleWeapon, self).remove()


class BasicEnemyWeapon(BasicWeapon):
    bullet_class = EnemyBullet
