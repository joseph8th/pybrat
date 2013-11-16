import os
from shutil import copy2, rmtree
from os.path import isfile, join, exists, basename, splitext

from pybrat.util import pv_mkdirs, pv_mkfile, pv_run_processes

from pybrat.define import PYBRAT_PATHS, PYBRAT_CONFD, PYBRAT_PROGD, \
    PYBRAT_ETCD, PYBRAT_SUBCMDD, PYBRAT_PROJD, PYBRAT_MAIND, PYBRAT_MAINF, \
    PYBRAT_CMD, PYBRAT_CMD_STR, PYBRAT_HOOKSD



class Installer(object):
    """ 
    Installs `pybrat` and some dependencies. 
    """

    def _install_pybrat(self, install_path):

        # makedirs
        for p in PYBRAT_PATHS:
            if not exists(p):
                print "Creating directory at: {}".format(p)
                if not pv_mkdirs(p):
                    return False

        # copy python scripts to ~/.pybrat/scripts/
        fdict = {}
        for root, dirs, files in os.walk(install_path):
            # in /scripts/ dir
            if basename(root) == 'scripts':
                del dirs[dirs.index('installer')]
                fdict['scripts'] = {}
                for f in files:
                    fname, fext = splitext(f)
                    if 'install' not in fname:
                        if fext == '.py':
                            fdict['scripts'][f] = {'cpfrom': join(root, f), 
                                                   'cpto': PYBRAT_PROGD}
            if basename(root) == 'etc':
                fdict['etc'] = {}
                for f in files:
                    fname, fext = splitext(f)
                    if fext == '' and fname == 'bashrc':
                        fdict['etc'][f] = {'cpfrom': join(root, f), 
                                           'cpto': PYBRAT_ETCD}
            if basename(root) == 'hooks':
                fdict['hooks'] = {}
                for f in files:
                    fname, fext = splitext(f)
                    if fext == '.skel':
                        fdict['hooks'][f] = {'cpfrom': join(root, f),
                                             'cpto': PYBRAT_HOOKSD}
            # ...in the /scripts/pybrat/ dir
            if basename(root) == 'pybrat':
                fdict['pybrat'] = {}
                for f in files:
                    fname, fext = splitext(f)
                    if fext == '.py':
                        fdict['pybrat'][f] = {'cpfrom': join(root, f),
                                              'cpto': PYBRAT_PROGD}
            # ...in /scripts/pybrat/subcommands dir
            if basename(root) == 'subcommands':
                fdict['subcommands'] = {}
                for f in files:
                    fname, fext = splitext(f)
                    if fext == '.py':
                        fdict['subcommands'][f] = {'cpfrom': join(root, f),
                                                   'cpto': PYBRAT_SUBCMDD}
        # fix 'pybrat_main.py' target
        fdict['scripts'][PYBRAT_MAINF]['cpto'] = join(PYBRAT_MAIND, 
                                                      PYBRAT_MAINF)

        # copy the files!
        for file_d in fdict.values():
            for f in file_d.values(): 
                if isfile(f['cpfrom']):
                    copy2(f['cpfrom'], f['cpto'])
                    print "Copied:\t" + f['cpfrom'] + "\n\t==> " + f['cpto']

        # make command script and link into user path
        if not isfile(PYBRAT_CMD):
            print "Installing Pybrat command at:"
            print "\t{}".format(PYBRAT_CMD)
            
            if not pv_mkfile(PYBRAT_CMD, 0755, PYBRAT_CMD_STR):
                return False

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

            if args.uninstall:
                return True
            else:
                # then 'reinstall' was chosen so continue...
                args.install = True

        # do a regular install ... shell script checks first so don't worry
        if args.install:
            if not exists(PYBRAT_CONFD):
                print "\nInstalling Pybrat...\n"
                return self._install_pybrat(install_path)
            else:
                print "\nInstallation Error: Pybrat is already installed."
                return False
