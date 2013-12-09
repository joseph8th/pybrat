from os import listdir
from sys import modules
from os.path import splitext
from pybrat.pvparser import subparsers
from pybrat.define import PYBRAT_SUBCMDD
from pybrat import subcommands

class Subcommand(object):
    """
    Parent class for subcommands.
    """
    name = None
    description = ""
    help = ""
    
    def __init__(self):
        """
        Initialize subparser for given subcommand.
        """
        self.parser = subparsers.add_parser(name = self.name,
                                            description = self.description, 
                                            help = self.help)
    def run(self, args):
        """
        Sends parsed arguments to given subcommand's run_command() method.
        """
        self.run_command(args)


### load subcommands funcs ###

def _load_subcommand(name):
    subcommand = 'pybrat.subcommands.%s' % name
    if subcommand in modules:
        return
    try:
        __import__(subcommand)
    except ImportError:
        pass

def get_subcmd_list():
    """
    Assumes /subcommands/*.py are commands if '__' is not in filename.
    """
    return [fname for fname, fext in map(splitext, listdir(PYBRAT_SUBCMDD)) 
            if fext == '.py' and '__' not in fname]

def load_subcommands():
    """
    Load all subcommands.
    """
    subcmd_l = get_subcmd_list()
    for name in subcmd_l:
        _load_subcommand(name)
