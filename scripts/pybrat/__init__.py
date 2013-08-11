from pybrat.pvparser import parser
from pybrat.util import set_config
from pybrat.subcommand import load_subcommands

def main():
    if not set_config():
        exit("Pybrat not installed or configured. Run 'pybrat-install.py'.")
    load_subcommands()
    args = parser.parse_args()
    args.command.run(args)
        
