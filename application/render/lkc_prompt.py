#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" AppRender prompt """

import sys
import core.core as core


def usage():
    """ Usage function"""
    if len(sys.argv) != 6:
        sys.exit("python2 ../main.py prompt path arch src_arch config_file"
                 "config_file may be empty \"\" for default configuraiton ")


def main():
    """ Main function """
    usage()

    sep = "------"

    test = sys.argv[1]
    if test != "prompt":
        return

    path = sys.argv[2]
    arch = sys.argv[3]
    src_arch = sys.argv[4]
    config_file = sys.argv[5]

    print sep
    core_instance = core.AppCore()
    print "Instance core created -- continue"
    print sep

    if core_instance.init_test_environnement(path) == -1:
        print "The path : " + path + " is not correct -- stop"
        sys.exit(1)
    print "Correct path : " + path + " -- continue"
    print sep

    core_instance.init_memory(path, arch, src_arch, config_file, callback=None)
    print sep
    core_instance.goto_next_opt()
    print "\tOption \tValue "
    print "\t"+sep+"\t"+sep
    for i in range(10):
        print "\t"+core_instance.get_current_opt_name(),\
              "\t"+core_instance.get_current_opt_value()
        core_instance.goto_next_opt()
        print core_instance.items[core_instance.cursor].def_exprs


if __name__ == '__main__':
    main()
