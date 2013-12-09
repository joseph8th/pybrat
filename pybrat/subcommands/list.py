from pybrat.util import get_project_list
from pybrat.subcommand import Subcommand
from pybrat.define import PYBRAT_SHGREEN, PYBRAT_SHGRAY, PYBRAT_SHWHITE

class ListProject(Subcommand):
    name = "list"
    description = "List all pybrat projects (optional: list virtualenvs)."
    help = "list pybrat projects (or virtualenvs)"

    def __init__(self):
        super(ListProject, self).__init__()
        self.arg_group = self.parser.add_mutually_exclusive_group()
        self.arg_group.add_argument("-b", "--brew", action="store_true",
                                    help="list pythonbrew virtualenvs")
        self.arg_group.add_argument("-w", "--wrap", action="store_true",
                                    help="list virtualenvwrapper virtualenvs")
        self.arg_group.add_argument("-v", "--venv", 
                                    help="find wild virtualenvs on VENV (path)")
        self.arg_group.set_defaults(command=self)

    def run_command(self, args):
        # make list of pybrat projects
        if hasattr(args, 'command'):
            del args.command
        args_d = vars(args)

        # get the list for the given project & set list type
        proj_d = get_project_list(args_d)
        if not proj_d:
            print "No projects or venvs found."
            return True
        proj_t = ['venv',] if args_d['venv'] else [t for t in args_d.keys() 
                                               if args_d[t] is True]
        if not proj_t:
            proj_t = ['pybrat',]

        # list the projects and respect. pythons, venvs
        for proj in proj_d:
            if 'srcpath' in proj_d[proj]:
                print "{}".format(PYBRAT_SHGREEN) + "%-24s " % proj ,
                print "{}".format(PYBRAT_SHGRAY) + "(%s)" % proj_d[proj]['srcpath']
            for vname, venv in proj_d[proj]['venv'].iteritems():
                print "{}".format(PYBRAT_SHWHITE) ,
                print "%24s" % ("%s [%-5s]" % (vname, venv['python'])) ,
                print "{0}({1})".format(PYBRAT_SHGRAY, venv['vpath'])

        # all done?
        return True

ListProject()
