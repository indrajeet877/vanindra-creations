"""Composition helpers for One Dot."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/r2_one_dot')
from od import *

EMERALD, IVORY, GOLD, GOLD_LT, WHITE = '#0B2A20', '#F6F1E7', '#A8843A', '#D2B26A', '#FFFFFF'


def latin_art(P_, word='vanindra', gold_dot=True):
    w = set_word(word, P_)
    dots = [dot(P_, cx, cy) for (cx, cy) in w['dots']]
    return w, dots


def hindi_art(P_):
    h = set_hindi(P_)
    dots = [dot(P_, cx, cy) for (cx, cy) in h['dots']]
    return h, dots


def add_word(ink, path, dots, s, dx, dy, ink_col, dot_col):
    ink.add(place(path, s, dx, dy), ink_col)
    for d in dots:
        ink.add(place(d, s, dx, dy), dot_col)
