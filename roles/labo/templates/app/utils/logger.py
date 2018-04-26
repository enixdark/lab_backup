# coding: utf-8

import logging
from logging.config import fileConfig
import os
class Singleton(object):
    """
    Singleton interface:
    """
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass


class Logger(Singleton):

    def __init__(self, name='logger', format=None, level=logging.DEBUG):
        file = os.path.abspath(os.path.join( os.path.dirname(os.path.realpath(__file__)), '../config.ini'))
        try:
            fileConfig(file)
        except IOError, e:
            os.makedirs('/'.join(e.filename.split('/')[:-1]))
            fileConfig(file)
        self.logger = logging.getLogger(name)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
