from os.path import abspath, basename, exists
from pybrat.util import get_project_list, pv_mkvenv, pv_link_projs, pv_add_proj 
from pybrat.subcommand import Subcommand
        
class InitProject(Subcommand):
    name = "init"
    description = "Create new pybrat project link from given project dir and venv. " + \
        "Flags '-w' or '-v' will import 'virtualenv' to a new pythonbrew venv."
    help = "initialize given project using given virtualenv"

    def __init__(self):
        super(InitProject, self).__init__()
        self.parser.add_argument("project",
                                 help="your existing project directory")
        self.parser.add_argument("virtualenv",
                                 help="your existing pythonbrew venv (import with flags)")
        self.arg_group = self.parser.add_mutually_exclusive_group()
        self.arg_group.add_argument("-w", "--wrap", action="store_true",
                                    help="virtualenvwrapper venv NAME (not path)")
        self.arg_group.add_argument("-v", "--venv", action="store_true",
                                    help="wild virtualenv PATH (rel. or abs.)")
        self.parser.set_defaults(command=self)

    def run_command(self, args):
        # validate the project dir to target for ln in .pybrat/projects
        proj_dir = abspath(args.project)
        vname = args.virtualenv if not args.venv else basename(args.virtualenv)
        print "Initializing project '{}'...".format(proj_dir)
        if not exists(proj_dir):
            print "Init Error: project directory '{}' not found.".format(proj_dir)
            return False

        # do we need to import given venv to pythonbrew first?
        if args.wrap or args.venv:
            if args.wrap:
                venv_d = (get_project_list({'wrap':True,}))['wrap']['venv']
            elif args.venv:
                venv_d = (get_project_list({'venv':args.virtualenv,}))['venv']['venv']
                args.virtualenv = basename(args.virtualenv)
            if vname in venv_d.keys():
                venv = venv_d[vname]
                # make pythonbrew venv
                print "Importing ({}) [{}] to pythonbrew...".format(vname, venv['python'])
                venv_dir = pv_mkvenv(vname, venv['python'])
                if not venv_dir:
                    print "Make Error: unable to create venv {}.".format(proj_name)
                    return False

        # safe to get pythonbrew venv dict now...
        venv_d = (get_project_list({'brew':True,}))['brew']['venv']
        if args.virtualenv not in venv_d.keys():
            print "Init Error: venv '{}' not found.".format(args.virtualenv)
            return False
        venv_dir = venv_d[args.virtualenv]

        # send to linking function
        if not pv_link_projs(venv_dir, proj_dir):
            print "Init Error: pythonbrew venv not linked to '{}'.".format(proj_dir)
            return False

        # add project link to .pybrat_projects/
        return pv_add_proj(proj_dir)

InitProject()
