from pygamii.objects import Object
import random
import time


class Gift(Object):
    _moving = True
    speed = 0
    expire_at = None
    created_at = None

    def __init__(self, *args, **kwargs):
        super(Gift, self).__init__(*args, **kwargs)
        self.created_at = time.time()

    def apply(self):
        pass

    def on_colision(self, obj):
        if obj is self.scene.airplane:
            self.apply()

    def move(self):
        if self.expire_at:
            if time.time() - self.created_at > self.expire_at:
                self.is_kill = True


class LifeGift(Gift):
    color = 'magenta'
    width = 7
    height = 3
    expire_at = 3
    to_render = '\n'.join([
        ' ▆▆ ▆▆ ',
        '███▆███',
        '  ▀█▀  ',
    ])

    def __str__(self):
        return self.to_render

    def apply(self):
        self.scene.airplane.lives += 1
        self.is_kill = True


gifts = [LifeGift]


def get_gift():
    if random.randint(1, 10) == 2:
        return random.choice(gifts)
    return None
