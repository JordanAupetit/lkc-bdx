#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from gi.repository import GObject as gobject

import os
import sys

class Callback(): 
    def __init__(self, callback):
        self.callback = callback
        self.stopped = False
        
    def update(self, progress):
        gobject.idle_add(self.callback, progress)

    """ pour stop le thread """
    def stop(self):
        self.stopped = True

    def stopped(self):
        return self.stopped
