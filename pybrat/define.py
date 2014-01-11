from os import environ, path

# Basic program globals
PYBRAT_VER = "0.2"
PYBRAT_PROG = "pybrat"
PYBRAT_PROG_VER = "pybrat-%s" % (PYBRAT_VER)
PYBRAT_PROG_DESCRIPTION="Wanna-Be Python Project Commander."

PYBRAT_PYVER = "2.7"

PYBRAT_INSTALL_ROOT = path.join( environ['HOME'], ".%s" % (PYBRAT_PROG) )


def get_pybrat_root(use_def=False):
    """
    Return pybrat root directory or correct parent of pwd
    """

    if 'PYBRAT_ROOT' in environ.keys():
        root = environ['PYBRAT_ROOT']
    else:
        root = PYBRAT_INSTALL_ROOT
    return root


# Pybrat root directories
PYBRAT_ROOT = get_pybrat_root()
PYBRAT_MAINF = path.join(PYBRAT_ROOT, "{}.py".format(PYBRAT_PROG))
PYBRAT_ETCD = path.join(PYBRAT_ROOT, "etc")
PYBRAT_HOOKSD = path.join(PYBRAT_ETCD, "hooks")

# Pybrat Python package source directories
PYBRAT_PROGD = path.join(PYBRAT_ROOT, PYBRAT_PROG)
PYBRAT_SUBCMDD = path.join(PYBRAT_PROGD, "subcommands")
PYBRAT_HACKSD = path.join(PYBRAT_PROGD, "hacks")

# User's 'home' project file directory
PYBRAT_PROJD = path.join(PYBRAT_ROOT, "home")

# prettify terminal
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

# virtualenvwrapper working globals
#PYBRAT_VWRAP_ROOTD = get_vwrap_root()


def get_pyenv_root():
    """
    Return pyenv root directory or none    """

    if 'PYENV_ROOT' in environ.keys():
        root = environ['PYENV_ROOT']
    else:
        root = ''
    return root


def get_pybrew_root():
    """
    Locate pythonbrew's root directory
    """

    root = None
    envpaths = environ['PATH'].split(':')

    for p in envpaths:
        if ".pythonbrew/bin" in p:
            root, pb_bin = path.split(p) 

    return root


def get_vwrap_root():
    """
    Locate virtualenvwrapper's venv directory
    """
    def_vw_root = path.join(environ['HOME'], ".virtualenvs")

    if 'WORKON_HOME' in environ:
        if exists(environ['WORKON_HOME']):
            return environ['WORKON_HOME']
    elif exists(def_vw_root):
        return def_vw_root
    else:
        return None
