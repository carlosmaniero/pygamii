from pygamii.objects import Object


class LiveScore(Object):
    x = 0
    width = 20

    def __str__(self):
        return 'Lives:' + '♥ ' * self.scene.airplane.lives


class Score(Object):
    x = 30
    width = 50
    points = 0

    def __str__(self):
        return 'Points: {}'.format(self.points)
