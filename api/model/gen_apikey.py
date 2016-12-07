# coding=utf-8
import hashlib
import random

__author__ = 'dolacmeo'
__doc__ = ''

ran_char = '0123456789' \
           'abcdefghijklmnopqrstuvwxyz' \
           'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
           '`~!@#$%^&*()-_=+\|[]{};:,.<>/?'


def gen_key(digit=32):
    return hashlib.md5("".join(random.sample(ran_char, digit))).hexdigest().upper()

if __name__ == '__main__':
    pass
