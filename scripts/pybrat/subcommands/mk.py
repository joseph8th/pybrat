from os.path import abspath, basename, exists
from pybrat.util import get_project_list, pv_mkdirs, pv_mkvenv, pv_link_projs, pv_add_proj 
from pybrat.subcommand import Subcommand

class MkProject(Subcommand):
    name = "mk"
    description = "Create and link NEW project directory and NEW virtualenv."
    help = "create new project and/or virtualenv(s) with given version(s) of python"


    def __init__(self):

        super(MkProject, self).__init__()

        self.parser.add_argument(
            "project",
            help="your NEW project directory and NEW venv name")
        self.parser.add_argument(
            "python", nargs='*',
            help="X.Y[.Z] python version(s) in order")
        self.parser.add_argument(
            "-v", "--venv", choices=['pyenv', 'pybrew'], default='pyenv',
            help="create new virtualenv(s) but no linked project")
        self.parser.add_argument(
            '-s', '--site', action="store_true",
            help="give new virtualenv(s) access to global site-packages")

        self.parser.set_defaults(command=self)


    def run_command(self, args):

        proj_name = basename(args.project)
        proj_dir = abspath(args.project)
        print "Making new project '%s' [%s]..." % (proj_dir, args.python)

        # check that project dir and venv don't exist
        if not args.venv:
            if exists(proj_dir):
                print "Make Error: '{}' already exists.".format(proj_dir)
                return False

        # make virtualenv
        venv_dir = pv_mkvenv(proj_name, args.python, args.venv, args.site)
        if not venv_dir:
            print "Make Error: unable to create venv {}.".format(proj_name)
            return False
        if args.venv:
            return True

        # make project dir
        if not pv_mkdirs(proj_dir):
            print "Make Error: unable to create {}.".format(proj_dir)
            return False

        # else everything set so link venv in project dir
        if not pv_link_projs(venv_dir, proj_dir):
            print "Init Error: venv not linked to '{}'.".format(proj_name)
            return False

        # add project link to .pybrat_projects/
        return pv_add_proj(proj_dir)

MkProject()
