#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from gi.repository import GObject as gobject


class Callback():
    def __init__(self, callback):
        self.callback = callback
        self.stopped = False

    def update(self, progress):
        gobject.idle_add(self.callback, progress)

    def stop(self):
        """ pour stop le thread """
        self.stopped = True

    def stopped(self):
        return self.stopped
