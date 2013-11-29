import os
from shutil import copy2, rmtree
from os.path import isfile, join, exists, basename, splitext

from pybrat.util import pv_mkdirs, pv_mkfile, pv_run_processes

from pybrat.define import PYBRAT_PATHS, PYBRAT_CONFD, PYBRAT_PROGD, \
    PYBRAT_ETCD, PYBRAT_SUBCMDD, PYBRAT_PROJD, PYBRAT_MAIND, PYBRAT_MAINF, \
    PYBRAT_CMD, PYBRAT_CMD_STR, PYBRAT_HOOKSD, PYBRAT_HACKSD, PYBRAT_INSTALLERD


class Installer(object):
    """ 
    Installs `pybrat` and some dependencies. 
    """

    def __init__(self):

        self.fdict_l = [
            { 'dname': 'scripts', 'fname_l': None, 'fext': '.py', 'target': PYBRAT_MAIND,
              'flist': [] },
            { 'dname': 'etc', 'fname_l': ['bashrc',], 'fext': '', 'target': PYBRAT_ETCD, 
              'flist': [] }, 
            { 'dname': 'hooks', 'fname_l': None, 'fext': '.skel', 'target': PYBRAT_HOOKSD, 
              'flist': [] }, 
            { 'dname': 'pybrat', 'fname_l': None, 'fext': '.py', 'target': PYBRAT_PROGD,
              'flist': [] },
            { 'dname': 'installer', 'fname_l': None, 'fext': '.py', 'target': PYBRAT_INSTALLERD,
              'flist': [] },
            { 'dname': 'subcommands', 'fname_l': None, 'fext': '.py', 'target': PYBRAT_SUBCMDD,
              'flist': [] },
            { 'dname': 'hacks', 'fname_l': None, 'fext': '.py', 'target': PYBRAT_HACKSD, 
              'flist': [] },
            ]


    def _set_fdict(self, root, files):
        # set src and dst for given root, files using fdict_l

        for fdict_d in self.fdict_l:
            if basename(root) == fdict_d['dname']:
                for f in files:

                    fname, fext = splitext(f)

                    if not fdict_d['fname_l']:
                        if fext == fdict_d['fext']:
                            fdict_d['flist'].append({'cpfrom': join(root, f), 
                                                     'cpto': fdict_d['target']})
                    else:
                        for sname in fdict_d['fname_l']:
                            if fext == fdict_d['fext'] and fname == sname:
                                fdict_d['flist'].append({'cpfrom': join(root, f), 
                                                         'cpto': fdict_d['target']})


    def _install_pybrat(self, install_path):

        # makedirs
        for p in PYBRAT_PATHS:
            if not exists(p):
                print "Creating directory at: {}".format(p)
                if not pv_mkdirs(p):
                    return False

        # copy python scripts to ~/.pybrat/scripts/
        for root, dirs, files in os.walk(install_path):
            self._set_fdict(root, files)

        # fix 'pybrat_main.py' target
#        self.fdict['scripts'][PYBRAT_MAINF]['cpto'] = join(PYBRAT_MAIND, 
#                                                      PYBRAT_MAINF)

        # copy the files!
        for fdict in self.fdict_l:
            for f in fdict['flist']:
####################333
                print f
                if isfile(f['cpfrom']):
########################3
#                    copy2(f['cpfrom'], f['cpto'])
                    print "Copied:\t" + f['cpfrom'] + "\n\t==> " + f['cpto']

        # make command script and link into user path
        if not isfile(PYBRAT_CMD):
            print "Installing Pybrat command at:"
            print "\t{}".format(PYBRAT_CMD)
########################33            
#            if not pv_mkfile(PYBRAT_CMD, 0755, PYBRAT_CMD_STR):
#                return False

        # all went well so print success screen
        print "\n-----------------------------------------------------\n" + \
            "*** Pybrat Install and Configuration is Complete. ***\n" + \
            "-----------------------------------------------------\n\n" + \
            "Add this to the END of your $HOME/.bashrc to add 'pybrat' " + \
            "to your command path:\n" + \
            "[[ -s \"$HOME/.pybrat/etc/bashrc\" ]] && " + \
            "source \"$HOME/.pybrat/etc/bashrc\"\n" 

        return True


    def installPybrat(self, install_path, args):
        """ 
        Create Pybrat user directories and copy scripts.
        """

        # check for default install action
        if True not in vars(args).values():
            args.install = True

        # if reinstall or uninstall then delete PYBRAT_CONFD
        if not args.install:
            if not exists(PYBRAT_CONFD):
                print "Uninstallation Error: Pybrat not installed."
                return False

            print "Uninstalling Pybrat installation..."
            for p in PYBRAT_PATHS:
                if p not in [PYBRAT_PROJD,]:
                    rmtree(p, ignore_errors=True)

            # if 'delete' option then remove projects directory, too
            if args.delete:
                print "Removing user project directory..."
                rmtree(PYBRAT_PROJD, ignore_errors=True)

            if args.uninstall or args.delete:
                return True
            else:
                # then 'reinstall' was chosen so continue...
                args.install = True

        # do a regular install ... shell script checks first so don't worry
        if args.install:
            print PYBRAT_CONFD
            if not exists(PYBRAT_CONFD):
                print "\nInstalling Pybrat...\n"
                return self._install_pybrat(install_path)
            else:
                print "\n==> ERROR: Pybrat is already installed."
                return False
