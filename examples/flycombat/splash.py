from pygamii.objects import Object, ToRenderMixin
from pygamii.action import MultipleMoveAction
from pygamii.scene import BaseScene


class Logo(ToRenderMixin, Object):
    to_render = '\n'.join([
        '    ________      ______                __          __ ',
        '   / ____/ /_  __/ ____/___  ____ ___  / /_  ____ _/ /_',
        '  / /_  / / / / / /   / __ \/ __ `__ \/ __ \/ __ `/ __/',
        ' / __/ / / /_/ / /___/ /_/ / / / / / / /_/ / /_/ / /_  ',
        '/_/   /_/\__, /\____/\____/_/ /_/ /_/_.___/\__,_/\__/  ',
        '        /____/                                         ',
    ])

    width = 55
    height = 6
    _moving = True
    red = True
    speed = 20
    y = -6
    color = 'green'

    def move(self):
        self.red = not self.red
        self.x = int(self.scene.cols / 2) - int(self.width / 2)

        if self.y != 10:
            self.y += 1
        else:
            self.speed = 4
            if self.red:
                self.color = 'red'
            else:
                self.color = 'green'


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
    y = -5
    speed = 10
    blink = 4
    cleaned = 0

    def move(self):
        self.x = int(self.scene.cols / 2) - int(self.width / 2)
        y = int(self.scene.rows / 2) - int(self.height / 2)

        if y != self.y:
            self.y += 1
        elif self.blink:
            self.speed = 5
            if self.color == 'blue':
                self.color = 'yellow'
            else:
                self.color = 'blue'
            self.blink -= 1
        elif self.scene.presents.centered:
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
    speed = 40
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


Scene().start()
