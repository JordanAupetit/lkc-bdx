#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" AppRender prompt """

import sys
import app_core


def usage():
    """ Usage function"""
    if len(sys.argv) != 5:
        sys.exit("python2 ./app_core_prompt.py path arch src_arch config_file"
                 "config_file may be empty \"\" for default configuraiton ")


def main():
    """ Main function """
    usage()

    sep = "------"

    path = sys.argv[1]
    arch = sys.argv[2]
    src_arch = sys.argv[3]
    config_file = sys.argv[4]

    print sep
    core = app_core.AppCore()
    print "Instance core created -- continue"
    print sep

    if core.init_test_environnement(path) == -1:
        print "The path : " + path + " is not correct -- stop"
        sys.exit(1)
    print "Correct path : " + path + " -- continue"
    print sep

    core.init_memory(path, arch, src_arch, config_file, callback=None)
    print sep

if __name__ == '__main__':
    main()
