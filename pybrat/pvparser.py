import argparse
from pybrat.define import PYBRAT_PROG, PYBRAT_PROG_VER, PYBRAT_PROG_DESCRIPTION

# instantiate arg parser
parser = argparse.ArgumentParser(prog=PYBRAT_PROG, description=PYBRAT_PROG_DESCRIPTION)
parser.add_argument("--version", action="version", version=PYBRAT_PROG_VER)
subparsers = parser.add_subparsers(
    title="subcommands", 
    description="for subcommand help, use '{} subcommand -h'".format(PYBRAT_PROG))
