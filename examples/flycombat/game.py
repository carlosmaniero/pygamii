from pygamii.scene import BaseScene
from pygamii.audio import Audio
from pygamii.action import MultipleMoveAction
from score import LiveScore, Score
from enemies import EnemyGenerator
from player import Airplane, Keyboard


class Scene(BaseScene):
    gifts = []

    def __init__(self, **kwargs):
        super(Scene, self).__init__(**kwargs)

        self.cols, self.rows = self.get_terminal_size()
        self.rows -= 1

        self.score = Score()
        self.add_object(self.score)

        self.music = Audio('songs/music.ogg')
        self.music.play(True)

        self.airplane = Airplane(self)
        self.add_object(self.airplane)
        self.add_action(Keyboard)
        self.add_action(MultipleMoveAction)

        self.add_object(LiveScore())

        self.add_action(EnemyGenerator)

    def stop(self):
        super(Scene, self).stop()
        self.music.stop()

Scene().start()
