""" Few utility methods """
import os
import sys


def match(arch):
    """ Match additional ARCH setting """
    arch_list = list([["i386", "x86"],
        ["x86_64", "x86"], ["sparc32", "sparc"],
        ["sparc64", "sparc"], ["sh64", "sh"],
        ["tilepro", "tile"], ["tilegx", "tile"]])

    for arch_iter in arch_list:
        if arch == arch_iter[0]:
            os.environ["SRCARCH"] = arch_iter[1]
            return

    os.environ["SRCARCH"] = os.environ.get("ARCH")


def usage():
    """ Usage function """
    if len(sys.argv) < 2:
        sys.exit("Require an architecture")


def main():
    """ Main function """
    usage()

    os.environ["ARCH"] = sys.argv[1]
    match(sys.argv[1])

    return

if __name__ == '__main__':
    main()
    import kconfiglib

    path = "/net/travail/bthiaola/linux-3.13/"
    os.environ["srctree"] = path

    c = kconfiglib.Config(filename=path+"Kconfig", base_dir=path,
            print_warnings=True)

    print c.get_srcarch()
    print c.get_arch()
    print c.get_srctree()
