from pygamii.objects import Object


class Wall(Object):
    pass


class MoveWall(Object):
    to_render_1 = '\n'.join([
        '██████',
        '      ',
        ''
    ])
    to_render_2 = '\n'.join([
        '      ',
        '██████',
        ''
    ])
    control = True
    width = 6
    speed = 10
    _moving = True
    to_render = ''

    def move(self):
        self.bg_color = 'red'
        if self.control:
            to_render = self.to_render_1
        else:
            to_render = self.to_render_2

        self.to_render = to_render * int(self.scene.rows / 2)
        self.height = self.scene.rows

        self.control = not self.control

    def __str__(self):

        return self.to_render
