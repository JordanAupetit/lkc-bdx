#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" Main function """

import sys
import render.lkc_gtk as lkc_gtk
import render.lkc_prompt as lkc_prompt


def main():
    """ Main function"""
    if len(sys.argv) > 1:
        if sys.argv[1] != "prompt":
            lkc_gtk.main()
            return
        else:
            lkc_prompt.main()
            return

    lkc_gtk.main()

if __name__ == '__main__':
    main()
