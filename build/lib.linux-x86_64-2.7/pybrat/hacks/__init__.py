#from sys import modules
from os import listdir, sep
from os.path import join, isdir, dirname, splitext
from importlib import import_module

#from pybrat.util import get_module_list, load_module_list
from pybrat.define import PYBRAT_HACKSD


def load_hacks():
    dir_l = [join(PYBRAT_HACKSD, d) for d in listdir(PYBRAT_HACKSD) if isdir(join(PYBRAT_HACKSD, d))]
    for modpath in dir_l:
        name = modpath.split(sep)[-1]
        load_module_list("pybrat.hacks.{}".format(name), modpath)
    

### load subcommands funcs ###

def load_module(name):
    if name in modules:
        return
#    try:
    import_module(name)
#        __import__(name)
#    except ImportError:
#        print "Import Error."

        
def get_module_list(pkgname, modpath):
    """
    Assumes [modpath]/*.py are commands if '__' is not in filename.
    """
    return ["{0}.{1}".format(pkgname, fname) for fname, fext 
            in map(splitext, os.listdir(modpath)) 
            if fext == '.py' and '__' not in fname]
    

def load_module_list(pkgname, modpath):
    """
    Load all modules listed.
    """
    mod_l = get_module_list(pkgname, modpath)
    for name in mod_l:
        load_module(pkgname + '.' + name)

