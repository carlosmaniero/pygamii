from pygamii.scene import BaseScene
from pygamii.audio import Audio
from pygamii.action import MultipleMoveAction, EventAction
from score import LiveScore, Score
from enemies import EnemyGenerator
from player import Airplane, Keyboard
from walls import MoveWall


class Scene(BaseScene):
    gifts = []
    bg_color = 'blue'
    boss = None

    def __init__(self, **kwargs):
        super(Scene, self).__init__(**kwargs)
        self.events = EventAction()
        self.add_action(self.events)

        self.cols, self.rows = self.get_terminal_size()
        self.rows -= 1

        self.wall_left = MoveWall()
        self.wall_right = MoveWall()
        self.wall_right.x = self.cols - self.wall_right.width
        self.add_object(self.wall_left)
        self.add_object(self.wall_right)

        self.score = Score()
        self.add_object(self.score)

        self.music = Audio('songs/music.ogg')
        self.music.play(True)

        self.airplane = Airplane(self)
        self.add_object(self.airplane)
        self.add_action(Keyboard())
        self.add_action(MultipleMoveAction())

        self.add_object(LiveScore())

        self.enemy_generator = EnemyGenerator()
        self.add_action(self.enemy_generator)

    def stop(self):
        super(Scene, self).stop()
        self.music.stop()
