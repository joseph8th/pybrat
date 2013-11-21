import os

from pybrat.util import get_module_list, load_module_list
from pybrat.define import PYBRAT_HACKSD

def load_hacks():
    dir_l = [d for d in os.listdir(PYBRAT_HACKSD) if os.path.isdir(d)]
############
    print PYBRAT_HACKSD + ": ", dir_l
    for modpath in dir_l:
        load_module_list("pybrat.hacks.{0}".format(modpath), modpath)
    
