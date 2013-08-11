from os.path import abspath, basename, exists
from pybrat.util import get_project_list, pv_mkdirs, pv_mkvenv, pv_link_projs, pv_add_proj 
from pybrat.subcommand import Subcommand

class MkProject(Subcommand):
    name = "mk"
    description = "Create and link new project directory and new pythonbrew venv."
    help = "create new project and/or virtualenv using given python version"

    def __init__(self):
        super(MkProject, self).__init__()
        self.parser.add_argument("project",
                                 help="your new project directory and venv name")
        self.parser.add_argument("python",
                                 help="X.Y[.Z] python version (in 'Python-X.Y.Z')")
        self.parser.add_argument("-b", "--brew", action="store_true",
                                 help="create a pythonbrew venv but no project")
        self.parser.set_defaults(command=self)

    def run_command(self, args):
        proj_name = basename(args.project)
        proj_dir = abspath(args.project)
        print "Making new project '{}' (Python-{})...".format(proj_dir, args.python)
        # check that project dir and venv don't exist
        if not args.brew:
            if exists(proj_dir):
                print "Make Error: project directory '{}' already exists.".format(proj_dir)
                return False
        # make pythonbrew venv
        venv_dir = pv_mkvenv(proj_name, args.python)
        if not venv_dir:
            print "Make Error: unable to create venv {}.".format(proj_name)
            return False
        if args.brew:
            return True
        # make project dir
        if not pv_mkdirs(proj_dir):
            print "Make Error: unable to create directory {}.".format(proj_dir)
            return False
        # else everything set so link venv in project dir
        if not pv_link_projs(venv_dir, proj_dir):
            print "Init Error: pythonbrew venv not linked to '{}'.".format(proj_name)
            return False
        # add project link to .pybrat_projects/
        return pv_add_proj(proj_dir)

MkProject()
