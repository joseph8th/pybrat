from os import environ, path

# Basic program globals
PYBRAT_VER = "0.2"
PYBRAT_PROG = "pybrat"
PYBRAT_PROG_VER = "pybrat-%s" % (PYBRAT_VER)
PYBRAT_PROG_DESCRIPTION="Wanna-Be Python Project Commander."

PYBRAT_PYVER = "2.7"

# Pybrat root directories
PYBRAT_ROOT = path.dirname(path.dirname(path.realpath(__file__)))
PYBRAT_MAINF = path.join(PYBRAT_ROOT, "{}.py".format(PYBRAT_PROG))
PYBRAT_ETCD = path.join(PYBRAT_ROOT, "etc")
PYBRAT_HOOKSD = path.join(PYBRAT_ETCD, "hooks")

# Pybrat Python package source directories
PYBRAT_PROGD = path.join(PYBRAT_ROOT, PYBRAT_PROG)
PYBRAT_SUBCMDD = path.join(PYBRAT_PROGD, "subcommands")
PYBRAT_HACKSD = path.join(PYBRAT_PROGD, "hacks")

# User's 'home' project file directory
PYBRAT_PROJD = path.join(environ['HOME'], ".{}".format(PYBRAT_PROG))

# prettify terminal (to be ELIMINATED)
PYBRAT_SHGREEN="\033[01;32m"
PYBRAT_SHGRAY="\033[0;37m"
PYBRAT_SHWHITE="\033[1;37m"
PYBRAT_SHRED="\033[0;31m"
PYBRAT_SHYELLOW="\033[1;33m"


# working globals for hacks
#PYBRAT_PYENV_ROOTD = get_pyenv_root()
#PYBRAT_PYENV_VENVD = path.join(PYBRAT_PYENV_ROOTD, "versions")
#PYBRAT_PYBREW_ROOTD = get_pybrew_root()
#PYBRAT_PYBREW_VENVD = path.join(PYBRAT_PYBREW_ROOTD, "venvs")
#PYBRAT_PYBREW_PYD = path.join(PYBRAT_PYBREW_ROOTD, "pythons")

