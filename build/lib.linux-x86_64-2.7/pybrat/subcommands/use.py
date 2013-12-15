from os import environ
from os.path import join, exists, basename
from pybrat.util import get_project_list, pv_run_processes, pv_check_subd, \
    print_err
from pybrat.define import PYBRAT_PYBREW_PYD, PYBRAT_PROG
from pybrat.subcommand import Subcommand

class UseProject(Subcommand):
    name = "use"
    description="Use pybrat project (venv and/or python) in a subshell."
    help="use given pybrat project's linked python version and/or virtualenv"

    def __init__(self):
        super(UseProject, self).__init__()
        self.parser.add_argument("project",
                                help="use given pybrat project (unless '-p' flag set)")
        self.parser.add_argument("-v", "--venv",
                                help="use virtualenv 'VENV' (if multi-venv project)")
        self.parser.add_argument("-p", "--python", action="store_true",
                                help="ONLY use given python version (X.Y[.Z])")
        self.parser.set_defaults(command=self)

    def run_command(self, args):
        # check for PYTHONPATH in environ
        if not "PYTHONPATH" in environ:
            return print_err("could not find PYTHONPATH in the environ.")

        # check if given project name is pybrat project else treat as python version
        if args.python:
            venv = {'python':[args.project,]}
        else:
            proj_d = get_project_list({'pybrat':True,})
            if not args.project in proj_d.keys():
                return print_err("pybrat project '{}' not found.".format(args.project))

            proj = proj_d[args.project]
            # check project/.pybrat subdir integrity
            pv_subd = join(proj['srcpath'], ".{}".format(PYBRAT_PROG))
            pv_check_subd(pv_subd, args={'all':True})
            # check if project is multi-venv
            if not args.venv and len(proj['venv']) > 1:
                return print_err("use '-v VENV' option to use multi-venv project")
            # if multi-venv, check for the venv
            if not args.venv:
                venv = proj['venv'].values()[0]
            else:
                if args.venv not in proj['venv']:
                    return print_err("VENV '{}' not found".format(args.venv))
                venv = proj['venv'][args.venv]

        # venv_d all set? then set pythonbrew PYTHONPATH base...
        new_pypath = join( PYBRAT_PYBREW_PYD, 
                           "Python-{}".format(venv['python']) )
        if not exists(new_pypath):
            return print_err("could not find 'Python-{}'.".format(venv['python']))
        # ... and PATH setting...
        path_l = environ['PATH'].split(':')
        for p in path_l:
            if PYBRAT_PYBREW_PYD in p:
                del path_l[path_l.index(p)]
        path_l.insert(0, join(new_pypath, "bin"))
        new_path = ":".join(path_l)

        # set up environ variables dict (all subshells)
        envdict = { 'PYBRAT_PYTHONPATH':join(new_pypath, "lib"), 
                    'PYBRAT_PATHS':new_path,'PYBRAT_PYTHON':venv['python'], }
        # if activating a venv as well as a python...
        if not args.python:
            hooksd = join(pv_subd, "hooks")
            envdict.update({ 'PYBRAT_WORKD':proj['srcpath'],
                             'PYBRAT_VENV':basename(venv['vpath']), 
                             'PYBRAT_PROJ_HOOKSD':hooksd, })

        # execute subshell
        runok = pv_run_processes(exelist=[], envdict=envdict, bash=True)
        if not runok:
            return print_err("subshell process error")
        # if postdeactivate run in parent shell 
        if exists(join(hooksd, "postdeactivate")):
            if not pv_run_processes([[join(hooksd, "postdeactivate")],]):
                return print_err("postdeactivate subprocess failed")

        # all done?
        return True

UseProject()
