#!/usr/bin/env python
import curses

pairs = {}


def get_color_str(color):
    return getattr(curses, 'COLOR_{}'.format(color.upper()))


def get_color_pair(fg, bg=-1):

    if isinstance(fg, str):
        fg = get_color_str(fg)
    if isinstance(bg, str):
        bg = get_color_str(bg)

    pair_hash = '{}_{}'.format(fg, bg)
    if pair_hash in pairs:
        return curses.color_pair(pairs[pair_hash])
    else:
        pair_hash_id = len(pairs) + 1
        curses.init_pair(pair_hash_id, int(fg), int(bg))
        pairs[pair_hash] = pair_hash_id
        return get_color_pair(fg, bg)
