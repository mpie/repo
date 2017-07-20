# -*- coding: utf-8 -*-

"""
    DooFree Add-on
    Copyright (C) 2017 DooFree
"""


import os.path

files = os.listdir(os.path.dirname(__file__))
__all__ = [filename[:-3] for filename in files if not filename.startswith('__') and filename.endswith('.py')]


