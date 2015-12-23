# coding: utf-8
from __future__ import unicode_literals
try:
    import pygame
    have_pygame = True
except ImportError:
    have_pygame = False


if have_pygame:
    class Audio(object):
        file = None
        song = None

        def __init__(self, file=None, auto_loading=True, *args, **kwargs):
            if file:
                self.file = file

            if self.file is None:
                raise AssertionError("audio need a file")

            if auto_loading:
                self.load_file()

        def load_file(self):
            pygame.mixer.init()
            self.song = pygame.mixer.Sound(self.file)

        def play(self, loop=False):
            if loop:
                self.song.play(-1)
            else:
                self.song.play()

        def stop(self):
            self.song.stop()

        def set_volume(self, volume):
            self.song.set_volume(volume)

else:
    # Simple Interface to prevent crashs
    class Audio(object):
        file = None
        song = None

        def __init__(self, *args, **kwargs):
            print('pygame not found')

        def load_file(self):
            pass

        def play(self, loop=False):
            pass

        def stop(self):
            pass

        def set_volume(self, volume):
            pass
