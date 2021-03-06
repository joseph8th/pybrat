import os
from os.path import join, exists



def get_pybrew_root():
    """
    Locate pythonbrew's root directory
    """

    envpaths = os.environ['PATH'].split(':')

    for p in envpaths:
        if ".pythonbrew/bin" in p:
            pb_root, pb_bin = os.path.split(p) 

    if pb_root:
        return pb_root

    return None



def get_vwrap_root():
    """
    Locate virtualenvwrapper's venv directory
    """
    def_vw_root = join(os.environ['HOME'], ".virtualenvs")

    if 'WORKON_HOME' in os.environ:
        if exists(os.environ['WORKON_HOME']):
            return os.environ['WORKON_HOME']
    elif exists(def_vw_root):
        return def_vw_root
    else:
        return None

# Basic program globals
PYBRAT_VER = "0.1"
PYBRAT_PROG = "pybrat"
PYBRAT_PROG_VER = "pybrat-{}".format(PYBRAT_VER)
PYBRAT_PROG_DESCRIPTION="The Wannabe-Ultimate Pythonbrew Commander and Virtualenv Wrangler."

# Pybrat home directories
PYBRAT_CONFD = join(os.environ['HOME'], ".{}".format(PYBRAT_PROG))
PYBRAT_MAIND = join(PYBRAT_CONFD, "scripts")
PYBRAT_PROGD = join(PYBRAT_MAIND, PYBRAT_PROG)
PYBRAT_SUBCMDD = join(PYBRAT_PROGD, "subcommands")
PYBRAT_BIND = join(PYBRAT_CONFD, "bin")
PYBRAT_ETCD = join(PYBRAT_CONFD, "etc")
PYBRAT_HOOKSD = join(PYBRAT_ETCD, "hooks")
# User modifiable global
PYBRAT_PROJD =join(os.environ['HOME'], ".pybrat_projects")

# Pybrat main() script
PYBRAT_MAINF = "pybrat_main.py"

# Pybrat path list
PYBRAT_PATHS = [PYBRAT_CONFD, PYBRAT_MAIND, PYBRAT_PROGD, PYBRAT_SUBCMDD, 
                PYBRAT_BIND, PYBRAT_ETCD, PYBRAT_HOOKSD, PYBRAT_PROJD]

# Build pybrat's command script filepath, contents, and default exec path
PYBRAT_CMD = join(PYBRAT_BIND, PYBRAT_PROG)
PYBRAT_CMD_STR = "#!/usr/bin/env bash\n" + \
    "/usr/bin/python2 \"{0}/{1}\" \"$@\"\n".format(PYBRAT_MAIND, PYBRAT_MAINF)

# Build Pybrat /etc/bashrc for user to source
PYBRAT_RC = join(PYBRAT_ETCD, "bashrc")

# pythonbrew working globals
PYBRAT_PYBREW_ROOTD = get_pybrew_root()
PYBRAT_PYBREW_VENVD = join(PYBRAT_PYBREW_ROOTD, "venvs")
PYBRAT_PYBREW_PYD = join(PYBRAT_PYBREW_ROOTD, "pythons")

# virtualenvwrapper working globals
PYBRAT_VWRAP_ROOTD = get_vwrap_root()

# prettify terminal
PYBRAT_SHGREEN="\033[01;32m"
PYBRAT_SHGRAY="\033[0;37m"
PYBRAT_SHWHITE="\033[1;37m"
PYBRAT_SHRED="\033[0;31m"
PYBRAT_SHYELLOW="\033[1;33m"
