from pygamii.objects import Object, ToRenderMixin
from pygamii.audio import Audio
from weapon import AirPlaneBullet, EnemyBoomb


def change_move_action(boss):
    if boss.move_method == 'go_down':
        boss.move_method = 'shooting'
        Audio('songs/before-shot.ogg').play()
        boss.color = 'red'
    elif boss.move_method == 'shooting':
        boss.move_method = 'go_up'
        Audio('songs/sonar.ogg').play()
        boss.color = 'red'
    else:
        boss.move_method = 'go_down'
        Audio('songs/sonar.ogg').play()
        boss.color = 'red'


class Boom(Object):
    char = '█'
    color = 'white'

    def on_create(self):
        Audio('songs/final-explosion.ogg').play()


class Water(Object):
    char = '~'
    color = 'cyan'
    width = 28
    height = 1
    _moving = True
    speed = 20

    def move(self):
        self.x = self.scene.boss.x
        self.y = self.scene.boss.y + self.scene.boss.height
        if self.char == '~':
            self.char = '^'
        else:
            self.char = '~'


class Boss(ToRenderMixin, Object):
    to_render = render_left = '\n'.join([
        '                ▃▃▃          ',
        '                 █           ',
        '                ▄█▄          ',
        '                ███          ',
        '█▂   ▁▂▃▅██████████████████▄ ',
    ])
    render_right = '\n'.join([
        '          ▃▃▃                ',
        '           █                 ',
        '          ▄█▄                ',
        '          ███                ',
        ' ▄██████████████████▅▃▂▁   ▂█',
    ])

    color = 'red'
    x = 6
    width = 28
    height = 5
    _moving = True
    speed = 20
    y = 3
    down = True
    counter = 0
    down_speed = 30
    upper = False
    resistence = 20
    to_kill = False
    move_method = ''
    shots = 20
    times_on_up = 3
    can_be_killed = False
    shot_interval = 10
    lives = 3

    def go_down(self):
        if self.counter % self.down_speed == 0:
            if self.height != 2:
                self.height -= 1
            else:
                self.scene.events.trigger('boss_move_complete', self)
        self.counter = (self.counter + 1) % self.down_speed

    def go_up(self):
        if self.counter % self.down_speed == 0:
            if self.height != 5:
                self.height += 1
            else:
                if self.times_on_up == 0:
                    self.can_be_killed = False
                    self.scene.events.trigger('boss_move_complete', self)
                    self.times_on_up = 20
                    self.color = 'red'
        self.counter = (self.counter + 1) % self.down_speed

    def shooting(self):
        if self.x % self.shot_interval == 0:
            bullet = EnemyBoomb()
            bullet.y = self.y
            if self.to_render == self.render_left:
                bullet.x = self.x + 17
            else:
                bullet.x = self.x + 12
            self.shots -= 1
            if self.shots == 0:
                self.scene.events.trigger('boss_move_complete', self)
                self.shots = 20
            self.scene.add_object(bullet)

    def move(self):
        if self.height == 5:
            self.can_be_killed = True
            self.color = 167
        else:
            self.can_be_killed = False
            self.color = 'red'

        if self.to_render == self.render_left:
            self.x += 1
            if self.x + self.width + 6 == self.scene.cols:
                self.to_render = self.render_right
        else:
            self.x -= 1
            if self.x == 6:
                self.to_render = self.render_left

        if self.move_method:
            getattr(self, self.move_method)()

    def __str__(self):
        ret = super(Boss, self).__str__()
        return ret[:(self.width + 2) * self.height]

    def on_collision(self, obj):
        if isinstance(obj, AirPlaneBullet):
            if self.can_be_killed:
                self.shot_interval -= 2
                self.lives -= 1
                self.shots = 20 * 3 - self.lives
                self.can_be_killed = False
                self.height = 4
                if self.lives == 0:
                    self.scene.music.stop()
                    self.is_kill = True
                    self.scene.stop()
                else:
                    self.scene.events.trigger('boss_move_complete', self)
                    Audio('songs/explosion.ogg').play()
            obj.is_kill = True

    def on_create(self):
        self.scene.music.stop()
        self.scene.music = Audio('songs/intro.ogg')
        self.scene.music.play(True)
