#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" Main function """

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'core/'))
sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'sync/'))
sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'core/lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '.',
                             'core/lib/kconfiglib/'))
sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'render/'))

import lkc_gtk


def main():
    """ Main function"""
    lkc_gtk.main()

if __name__ == '__main__':
    main()
