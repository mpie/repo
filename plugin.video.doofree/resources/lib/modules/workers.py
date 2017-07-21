# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 DooFree
'''


import threading


class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)
