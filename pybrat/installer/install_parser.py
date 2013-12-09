import argparse
from pybrat.define import PYBRAT_PROG_VER, PYBRAT_PROG_VER
from install import Installer # installPybrat

def installparser():

    description = "Install {} in your $HOME dir.".format(PYBRAT_PROG_VER)
    parser_install = argparse.ArgumentParser(description=description)
    install_group = parser_install.add_mutually_exclusive_group()
    myInstaller = Installer()

    install_group.add_argument("-i", "--install", action="store_true",
                               help="DEFAULT: install %s" % (PYBRAT_PROG_VER))
    install_group.add_argument("-r", "--reinstall", action="store_true",
                               help="uninstall/install %s" % (PYBRAT_PROG_VER))
    install_group.add_argument("-u", "--uninstall", action="store_true",
                               help="uninstall %s but leave user data" % (PYBRAT_PROG_VER))
    install_group.add_argument("-d", "--delete", action="store_true",
                               help="uninstall %s and delete user data" % (PYBRAT_PROG_VER))

    # set callback method
    parser_install.set_defaults(func=myInstaller.installPybrat)


    return parser_install.parse_args()
