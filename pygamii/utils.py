#!/usr/bin/env python
import curses


def init_colors():
    for i in range(0, curses.COLORS):
        for j in range(0, curses.COLORS):
            curses.init_pair(curses.COLORS * (i + 1) + j, i, j)


def get_color_pair(fg, bg=None):
    if bg is None:
        bg = 'black'

    bg_index = getattr(curses, 'COLOR_{}'.format(bg.upper()))
    fg_index = getattr(curses, 'COLOR_{}'.format(fg.upper())) + 1

    return curses.color_pair(curses.COLORS * fg_index + bg_index)
