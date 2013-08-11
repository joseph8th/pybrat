import argparse
from pybrat.define import *
from installer.install import installPybrat

def installparser():
    description = "Install {} in your $HOME dir.".format(PYBRAT_PROG_VER)
    parser_install = argparse.ArgumentParser(description=description)
    install_group = parser_install.add_mutually_exclusive_group()
    install_group.add_argument("-i", "--install", action="store_true",
                               help="DEFAULT: install {}".format(PYBRAT_PROG_VER))
    install_group.add_argument("-r", "--reinstall", action="store_true",
                               help="uninstall/install {}".format(PYBRAT_PROG_VER))
    install_group.add_argument("-u", "--uninstall", action="store_true",
                               help="uninstall {}".format(PYBRAT_PROG_VER))
    parser_install.set_defaults(func=installPybrat)

    return parser_install.parse_args()
