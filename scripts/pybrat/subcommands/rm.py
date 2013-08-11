from os import readlink, remove
from os.path import join, exists
from shutil import rmtree
from pybrat.util import get_project_list, get_input_bool, pv_rmvenv, pb_rmvenv
from pybrat.define import PYBRAT_PROJD, PYBRAT_PROG
from pybrat.subcommand import Subcommand

class RmProject(Subcommand):
    name = "rm"
    description = "Remove pybrat project (leaves your project directory alone)."
    help = "remove given project and/or virtualenv(s)"

    def __init__(self):
        super(RmProject, self).__init__()
        self.parser.add_argument("project",
                                 help="pybrat project or venv to remove (mod with flags)")
        self.parser.add_argument("-v", "--venv", action="store_true",
                                 help="ALSO delete any venvs linked to 'project'")
        self.parser.add_argument("-b", "--brew", action="store_true",
                                 help="ONLY delete pythonbrew venv named 'project'")
        self.parser.set_defaults(command=self)

    def run_command(self, args):
        # rm venv 'project' ONLY
        if args.brew:
            vname = args.project
            print "Deleting given pythonbrew virtualenv '{}' ONLY...".format(vname)
            # check if target venv is linked in pybrat project
            proj_d = get_project_list({'pybrat': True,})
            for proj in proj_d.keys():
                if vname in proj_d[proj]['venv'].keys():
                    pv_proj_dir = proj_d[proj]['srcpath']
                    print "Venv '{0}' is being used by project '{1}'.".format(vname, proj)
                    print "Deleting it will break a link unless you delete the link too."
                    if get_input_bool("Cleanup the pybrat project as well? [y/N] ",
                                      default_answer=False):
                        # rm venv and cleanup project
                        if not pb_rmvenv(vname, pv_proj_dir):
                            print "Remove Error: {} was not deleted".format(args.project)
                            return False
                        return True
            # venv not in any pybrat project so no worries...
            if not pb_rmvenv(vname):
                print "Remove Error: {} was not deleted".format(args.project)
                return False
            return True

        # still here? then delete the rest of the pybrat project...
        pv_projd = join(PYBRAT_PROJD, args.project)
        if not exists(pv_projd):
            print "Remove Error: {} does not exist".format(pv_projd)
            return False
        print "==> Removing project '{}'...".format(args.project)

        # if 'pythonbrew venv delete project'...?
        if args.venv:
            print "Deleting linked virtualenv(s)..." 
            if not pv_rmvenv(pv_projd):
                print "Remove Error: {} was not deleted".format(pv_projd)
                return False

        # remove .pybrat dir in user's project dir
        pv_subd = join(readlink(pv_projd), ".{}".format(PYBRAT_PROG))
        if not exists(pv_subd):
            print "Remove Error: {} does not exist.".format(pv_subd)
            return False
        rmtree(pv_subd, ignore_errors=True)
        print "Removed .pybrat subdirectory {}".format(pv_subd)

        # remove pybrat project link in .pybrat_projects/
        remove(pv_projd)
        print "Removed pybrat project {}".format(pv_projd)

        # all done deleting shit? ok...
        return True

RmProject()
