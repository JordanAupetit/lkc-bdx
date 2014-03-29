#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from gi.repository import GObject as gobject

import os
import sys

class Callback(): 
    def __init__(self, callback):
        self.callback = callback
        
    def update(self, progress):
        gobject.idle_add(self.callback, progress)
