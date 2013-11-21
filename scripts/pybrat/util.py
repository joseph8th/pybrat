import os
import sys
from os.path import join, exists, basename, islink, isfile, isdir, \
    splitext
import shutil
import subprocess
from pybrat.define import *

### general purpose funcs ###

def print_err(msg, warning=False, post_exit=False):
    err_type = 'WARNING' if warning else 'ERROR'
    err_color = PYBRAT_SHYELLOW if warning else PYBRAT_SHRED
    err_msg = "{0}{1}: {2}".format(err_color, err_type, msg)
    if post_exit:
        exit(err_msg)
    print >> sys.stderr, err_msg
    return False



### load subcommands funcs ###

def load_module(name):
    if name in sys.modules:
        return
    try:
        __import__(name)
    except ImportError:
        print "Import Error."
#        pass

        
def get_module_list(pkgname, modpath):
    """
    Assumes [modpath]/*.py are commands if '__' is not in filename.
    """
    return ["{0}.{1}".format(pkgname, fname) for fname, fext 
            in map(splitext, os.listdir(modpath)) 
            if fext == '.py' and '__' not in fname]
    

def load_module_list(pkgname, modpath):
    """
    Load all modules listed.
    """
    mod_l = get_module_list(pkgname, modpath)
    for name in mod_l:
        load_module(pkgname + '.' + name)



### other generic funcs ###

def get_input_bool(question, default_answer):
    """
    Get user input.     """

    ansstr = raw_input("\n{0}{1}".format(PYBRAT_SHGREEN, question))
    print "{}".format(PYBRAT_SHGRAY)
    ans = default_answer
    if ansstr:
        if 'y' in ansstr.lower()[0]:
            ans = True
        elif 'n' in ansstr.lower()[0]:
            ans = False
    return ans
        

### check if config is set ###
def set_config():
    retval = True
    if not 'HOME' in os.environ:
        retval = False
    else:
        if not isfile(PYBRAT_CMD):
            print "Pybrat command script not found in pythonbrew path at:"
            print "\t{}".format(PYBRAT_CMD)
            retval = False
        for p in [PYBRAT_CONFD, PYBRAT_MAIND, PYBRAT_PROJD]:
            if not exists(p):
                print "Directory not found at: {}".format(p)
                retval = False
    return retval


### file/dir utils ###

def pv_mkdirs(target):
    try:
        os.makedirs(target, 0755)
    except os.error as e:
        print "Error({0}): {1}".format(e.errno, e.strerror)
        return False
    else:
        return True


def pv_mkfile(target, mode, data):
    try:
        cmdfile = open(target, 'wb')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        return False
    else:
        cmdfile.write(data)
        cmdfile.close()
        os.chmod(target, mode)
        return True


def pv_symlink(source_file, link_name):
    if not exists(source_file):
        print "Symlink Error: {} does not exist.".format(source_file)
        return False
    if exists(link_name):
        print "Symlink Error: {} already exists.".format(link_name)
        if not get_input_bool("Replace existing link with new one? [y/N]: ",
                              default_answer=False):
            return False
        else:
            try:
                os.remove(link_name)
            except OSError as e:
                print "OS error({0}): {1}".format(e.errno, e.strerror)
                return False
    os.symlink(source_file, link_name)
    return True


def pv_check_subd(pv_subd, args={}):
    if not exists(pv_subd):
        return

    # if integrity check...
    if 'all' in args:
        args = {'hooks':True,}

    # check if hooks dir is OK
    if 'hooks' in args:
        hooksd = join(pv_subd, "hooks")
        if not exists(hooksd):
            print "Creating 'hooks' dir at '{}'".format(hooksd)
            if not pv_mkdirs(hooksd):
                print_err("unable to create 'hooks' directory", 
                          post_exit=True)
            for f in os.listdir(PYBRAT_HOOKSD):
                shutil.copy2(join(PYBRAT_HOOKSD, f), join(hooksd, f))
                print "Copied:\t{0}\n\t==> {1}".format(
                    join(PYBRAT_HOOKSD, f), join(hooksd, f))
                            
    # check if multi-venv or multi-
    if 'vname' in args:
        old_pyd_l = [join(pv_subd, pyd) for pyd in os.listdir(pv_subd) 
                     if 'python' in pyd.lower() 
                     and isdir(join(pv_subd,pyd))] 
        if old_pyd_l:
            print "{}".format(PYBRAT_SHWHITE) + "%-9s" % "WARNING:" + \
                "other Python(s) are already attached to this project!"
            print  "{}".format(PYBRAT_SHGRAY) + "%-9s" % "OPTIONS:" + \
                "(1) make '%s' a single-venv project, OR" % (args['proj'])
            print "%-9s(2) add '%s' to a list in a multi-venv project.\n" \
                % ("", args['vname'])
            print "{}".format(PYBRAT_SHWHITE) + \
                "[y]: YES, purge old links and replace with '%s'." \
                % (args['vname'])
            print "[N]: NO, don't purge and replace. " + \
                "Add new venv '%s' to a list of linked venvs." & \
                (args['vname'])
            prompt = "Purge old venv links and replace with new one? [y/N]: "
            
            # if add venv to list then just return leaving .pybrat untouched
            if not get_input_bool(prompt, default_answer=False):
                print "\nAdding '%s' to list of venvs " % (args['vname']) + \
                    "in '%s'..." % (args['proj'])
            # ...else purge .pybrat subdir first then return
            else:
                print "\nPurging old venvs in '{}'...".format(args['proj'])
                for pyd in old_pyd_l:
                    shutil.rmtree(pyd, ignore_errors=True)


def pv_add_proj(proj_dir):
    proj_name = basename(proj_dir)
    # check if project/.pybrat subdir 'etc' (non-venv) reqs are OK
    pv_check_subd(join(proj_dir, ".{}".format(PYBRAT_PROG)), args={'hooks':True})
    # link to project dir in .pybrat_projects/project
    if not pv_symlink(proj_dir, join(PYBRAT_PROJD, proj_name)):
        return False
    print "Linked:\t" + join(PYBRAT_PROJD, proj_name) + "\n\t--> " + proj_dir
    return True


def pv_link_projs(venv_dir, proj_dir):
    proj_name = basename(proj_dir)
    venv_name = basename(venv_dir['vpath'])
    # what to do if .pybrat subdir already has venv(s)?
    pv_subd = join( proj_dir, ".{}".format(PYBRAT_PROG) ) 
    pv_check_subd(pv_subd, {'proj':proj_name, 'vname':venv_name})
    # duplicate pythonbrew Python-X.Y.Z directory structure
    pv_py_subd = join( pv_subd, "Python-{}".format(venv_dir['python']), )
    # create .pybrat hidden subdir in project dir
    if not pv_mkdirs(pv_py_subd):
        return print_err("directory(s) not created", warning=True)
    # link to pythonbrew Python-X.Y.Z dirs in .pybrat subdir
    if not pv_symlink(venv_dir['vpath'], join(pv_py_subd, venv_name)):
        return print_err("venv not linked to project", warning=True)
    print "Linked:\t" + pv_py_subd +"/"+ venv_name + "\n\t--> " + venv_dir['vpath']
    return True



### general purpose proj/venv utils ###


#def _get_pyenv_venv_list():
#    venv_d = {}
#    for python in os.listdir(PYBRAT_PYENV_VENVD):
#        for vname in os.listdir(join(PYBRAT_PYENV_VENVD, python)):


def _get_pybrew_venv_list():
    venv_d = {}
    for python in os.listdir(PYBRAT_PYBREW_VENVD):
        for vname in os.listdir(join(PYBRAT_PYBREW_VENVD, python)):
            venv_d[vname] = {'vpath':join(PYBRAT_PYBREW_VENVD, 
                                          python, vname),
                             'python':python.lower().strip('python-')}
    return { 'brew': {'abspath': PYBRAT_PYBREW_VENVD, 'venv':venv_d}, }



def _get_vwrap_venv_list():
    venv_d = {}
    vw_venv_l = [p for p in os.listdir(PYBRAT_VWRAP_ROOTD) 
                 if isdir(join(PYBRAT_VWRAP_ROOTD, p))]
    for vname in vw_venv_l:
        vpath = join(PYBRAT_VWRAP_ROOTD, vname)
        if exists(join(vpath, "include")):
            for python in os.listdir(join(vpath, "include")):
                if 'python' in python.lower():
                    venv_d[vname] = {'vpath':vpath,
                                     'python':python.lower().strip('python-')}
    return { 'wrap': {'abspath': PYBRAT_VWRAP_ROOTD, 'venv':venv_d}, }



def _get_wild_venv_list(sroot):
    venv_d = {}
    spath = abspath(sroot)
    if not exists(spath):
        return venv_d
    for root, dirs, files in os.walk(spath):
        subd_d = {}
        for subd in dirs:
            if subd in ['include', 'lib', 'bin']:
                subd_d[subd] = join(root, subd)
        if len(subd_d) == 3:
            py_l = [py.lower().strip('python-') for py in os.listdir(subd_d['include'])
                    if 'python' in py.lower()]
            for python in py_l:
                vname = basename(root)
                venv_d[vname] = {'vpath':root, 'python':python,}
    return { 'venv': {'abspath':spath, 'venv':venv_d,}, }



def _get_pybrat_proj_list():
    proj_d = {}
 
   # get each source dir linked to in .pybrat_projects/*
    for project in sorted(os.listdir(PYBRAT_PROJD)):

        # pybrat ln to proj
        proj_ln = join(PYBRAT_PROJD, project)
        if not islink(proj_ln):
            continue

        # orig user proj path
        proj_srcd = os.readlink(proj_ln)

        # project/.pybrat dir 
        proj_pvd = join(proj_srcd, ".{}".format(PYBRAT_PROG))

        # check if .pybrat subdir exists in source dir
        if not exists(proj_pvd):
            proj_venv_d = {'*': {'vpath':"*", 'python':"*"},}
            if not exists(proj_srcd):
                proj_srcd = "*"
        else:
            proj_pyver_l = [ py.lower().strip('python-') 
                             for py in os.listdir(proj_pvd) 
                             if 'python' in py.lower() ]

            # check if python subdir(s) exists in .pybrat/
            if not proj_pyver_l:
                proj_venv_d = {'*': {'vpath':"*", 'python':"*"},}
            else:
                proj_venv_d = {}

                for python in proj_pyver_l:
                    pyd = join(proj_pvd, "Python-{}".format(python))
                    venv_l = [ venv for venv in os.listdir(pyd) 
                               if islink(join(pyd, venv)) ]

                    # check if venv subdir link(s) exists in .pybrat/Python-*
                    if venv_l:
                        for vname in venv_l:

                            # check if link resolves to real source dir
                            vpath = os.readlink(join(pyd, vname))
                            if not exists(vpath):
                                vname = "*"
                                vpath = "*"

                            # got vals for every key? add to proj venv dict
                            proj_venv_d[vname] = {'vpath':vpath,
                                                  'python':python,}

        # everything OK per project? then set project dict entry
        if proj_venv_d:
            proj_d[project] = { 'abspath': proj_ln,
                                'srcpath': proj_srcd, 
                                'venv':proj_venv_d, }

    # return the result
    return proj_d



def get_project_list(args):
    # list pythonbrew venv project directories and pythons
    if 'brew' in args and args['brew']:
        return _get_pybrew_venv_list()
    # list virtualenvwrapper's ~/.virtualenvs projects if they exist
    elif 'wrap' in args and args['wrap']:
        return _get_vwrap_venv_list()
    elif 'venv' in args and args['venv']:
        return _get_wild_venv_list(args['venv'])
    # DEFAULT: list pybrat projects in .pybrat_projects/*
    else:
        return _get_pybrat_proj_list()



def get_venv_dict(args):
    if 'wrap' in args and args['wrap']:
        venv_d = (get_project_list({'wrap':True,}))['wrap']['venv']
    elif 'venv' in args and args['venv']:
        venv_d = (get_project_list({'venv':args.virtualenv,}))['venv']['venv']
        args.virtualenv = os.path.basename(args.virtualenv)
    elif 'brew' in args and args['brew']:
        venv_d = (get_project_list({'brew':True,}))['brew']['venv']
    elif 'pybrat' in args and args['pybrat']:
        proj_d = get_project_list({'pybrat':True,})
        if args['pybrat'] in proj_d.keys():
            venv_d = proj_d[args['pybrat']]['venv']
        else:
            venv_d = {}
    else:
        venv_d = {}
    return venv_d



def get_venv(args):
    venv_d = get_venv_dict(args)
    if args['vname'] not in venv_d.keys():
        print "Init Error: venv '{}' not found.".format(args['vname'])
        return None
    return venv_d[args['vname']]



### functions that run shell commands in subprocesses ###

def pv_run_processes(exelist=None, envdict=None, shell=True, bash=False):
    # change environ of subprocess if nec.
    env = os.environ.copy()
    if envdict:
        for var, val in envdict.iteritems():
            env[var] = val

    # execute command in subshell or subprocess
    if bash:
        print "{0}==> Entered pybrat subshell. {1}".format(
            PYBRAT_SHGREEN, PYBRAT_SHWHITE),
        print "Enter 'deactivate' to exit.{}".format(PYBRAT_SHGRAY)
        print "# Enter 'home' to change to project dir. Enter 'prompt' to toggle prompt."
        os.environ.update(env)
        os.system('bash -l')
        print "{0}==> Exited pybrat subshell.{1}".format(
            PYBRAT_SHGREEN, PYBRAT_SHGRAY)

    # exec command in subprocess
    else:
        for exe in exelist:
            if shell:
                exe = " ".join(exe)
            print "{}==> Executing command '".format(PYBRAT_SHGREEN), exe, \
                "'...{}".format(PYBRAT_SHGRAY)
            subproc = subprocess.Popen(exe, env=env, shell=shell,
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.STDOUT)
            pout, perr = subproc.communicate()
            if pout:
                print pout
            if perr:
                print perr
                return False
            print "{0}==> Execution complete.{1}".format(PYBRAT_SHGREEN, 
                                                         PYBRAT_SHGRAY)

    # all done executing commands? ok...
    return True


def pv_check_python(python):

    print "Looking for Python-%s ..." % python

    # get list of known pythons from pythonbrew
    subproc = subprocess.Popen(
        "pythonbrew list -k".split(),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    pout, perr = subproc.communicate()
    if perr:
        print perr
        return False

    pb_py_l = [py.lower().strip('python-') for py in pout.split() 
               if 'Python-' in py] 

    # if given python not in list give up...
    if not python in pb_py_l:
        print "ERROR: 'Python-%s' not known by pythonbrew." % python
        print "(Tip: run 'pythonbrew update' and try again.)\n" 
        print pout
        return False

    # ...else ask to install it
    if not get_input_bool(
            "This version available. Do you want to install it? [y/N]: ",
            default_answer=False):
        return False

    print "This might take a while. Please try to be patient..."

    if not pv_run_processes([['pythonbrew', 'install', python],]):
        print "ERROR: pythonbrew subprocess(es) failed."
        return False

    return True



def pv_mkvenv(vname, python, venv, site=False):
    """ 
    Function to create virtualenv(s) using given 'venv' method.
    """

    venv_d = (get_project_list({'brew':True,}))['brew']['venv']

    # check if target python version exists or needs to be installed
    if "Python-{}".format(python) not in os.listdir(PYBRAT_PYBREW_PYD):
        print "Error: target pythonbrew 'Python-%s' is not installed." \
            % (python)

        if not pv_check_python(python):
            return None

    # construct the pythonbrew command now before the logic following...
    proc_l = ['pythonbrew', 'venv', 'create', vname, '-p', python]
    if site:
        proc_l.append('-g')

    # check if target venv name already exists in pythonbrew
    if vname in venv_d:
        pb_venv = venv_d[vname]

        if not pb_venv['python'] == python:
            print "Error: venv with same name, but version %s exists." \
                % (pb_venv['python'])
            return None
        else:
            print "Error: venv '%s' [%s] already exists!" \
                % (vname, pb_venv['python'])
            return None

    # otherwise create the venv with pythonbrew
    elif not pv_run_processes( [proc_l,] ):
        print "Error: pythonbrew subprocess(es) failed."
        return None

    # reload the venv from the project list to be sure & return it
    venv_d = (get_project_list({'brew':True,}))['brew']['venv']
    if vname in venv_d:
        return venv_d[vname]

    # otherwise return nada
    return None



def pb_rmvenv(vname, proj_dir=None):
    venv_d = (get_project_list({'brew':True,}))['brew']['venv']
    if not vname in venv_d.keys():
        print "Delete Venv Error: virtualenv not found."
        return False
    python = venv_d[vname]['python']
    # use pybrew to delete the venv
    if not pv_run_processes(
            [['pythonbrew', 'venv', 'delete', vname, '-p', python],]):
        print "Error: pythonbrew subprocess(es) failed."
        return False
    # clean up if linked to a project...
    if proj_dir:
        pv_pyd = join(proj_dir, ".{}".format(PYBRAT_PROG), 
                      "Python-{}".format(python))
        os.remove(join(pv_pyd, vname))
        if not os.listdir(pv_pyd):
            os.rmdir(pv_pyd)
    # all done...
    return True


def pv_rmvenv(proj_dir):
    proj = basename(proj_dir)
    proj_d = get_project_list({'pybrat':True,})
    # rm pybrew venv(s)
    venv_d = proj_d[proj]['venv']
    for vname, venv in venv_d.iteritems():
        if not pb_rmvenv(vname, proj_dir):
            return False
    return True
