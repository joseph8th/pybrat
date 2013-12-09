######################################################
##### A WORK IN PROGRESS! (DON'T PUT IN GIT YET) #####
######################################################

import os
import sys
import shutil
from cStringIO import StringIO            # to redirect stdout
from argparse import Namespace
from pybrat.subcommand import Subcommand
from pybrat.util import get_project_list, get_venv_dict, pv_mkdirs
from pybrat.define import PYBRAT_SHGREEN, PYBRAT_SHGRAY, PYBRAT_SHWHITE, PYBRAT_SHRED

### Test classes ###

class Args(object):
    def __init__(self, args_d):
        for (k,v) in args_d.items():
            setattr(self, k, v)


class PybratTest(object):
    name = None
    subcmd = None

    def run(self, args, outcome):
        print "{}Testing '{}' ".format(PYBRAT_SHWHITE, self.name),
        result = (outcome == self.run_tests(Args(args)))
        return result

    def run_subcmd(self, args):
        sys.stdout = testout = StringIO()
        self.subcmd.run_command(args)
        sys.stdout = sys.__stdout__
        return testout

class ListTest(PybratTest):
    name = 'list'

    def __init__(self):
        super(ListTest, self).__init__()
        from pybrat.subcommands.list import ListProject
        self.subcmd = ListProject()

    def run_tests(self, args):
        print "for '{}'...{}".format(args.project, PYBRAT_SHGRAY)
        testout = self.run_subcmd(args)
        if args.verbose > 1:
            print testout.getvalue()
        testout_l = testout.getvalue().split('\n')
        found_l = [l for l in testout_l if args.project in l]
        if found_l:
            if args.verbose:
                print "==> Found '{}' in list item(s):".format(args.project)
                for line in found_l:
                    print "    -> {}".format(line[:75] + (line[75:] and '...'))
            return True
        else:
            return False


class InitTest(PybratTest):
    name = 'init'

    def __init__(self):
        from pybrat.subcommands.init import InitProject
        super(InitTest, self).__init__()
        self.subcmd = InitProject()

    def run_tests(self, args):
        print "for '{}'...{}".format(args.project, PYBRAT_SHGRAY)
        testout = self.run_subcmd(args)
        if args.verbose > 1:
            print testout.getvalue()
        proj_d = get_project_list({'pybrat':True})
        result = True
        if args.project in proj_d.keys():
            if args.verbose:
                print "==> Found '{}' project.".format(args.project)
        else:
            result = False
        if args.virtualenv in proj_d[args.project]['venv']:
            if args.verbose:
                print "==> Found '{}' venv.".format(args.virtualenv)
        else:
            result = False
        return result


class MkTest(PybratTest):
    name = 'mk'

    def __init__(self):
        super(MkTest, self).__init__()
        from pybrat.subcommands.mk import MkProject
        self.subcmd = MkProject()

    def run_tests(self, args):
        print "for '{}'...{}".format(args.project, PYBRAT_SHGRAY)
        testout = self.run_subcmd(args)
        if args.verbose > 1:
            print testout.getvalue()
        if args.project in get_venv_dict({'brew':True}).keys():
            if args.verbose:
                print "==> Found '{}' venv.".format(args.project)
            result = True
        else:
            result = False
        if not args.brew:
            if args.project in get_project_list({'pybrat':True}).keys():
                if args.verbose:
                    print "==> Found '{}' project.".format(args.project)
            else:
                result = False
        return result


class RmTest(PybratTest):
    name = 'rm'

    def __init__(self):
        super(RmTest, self).__init__()
        from pybrat.subcommands.rm import RmProject
        self.subcmd = RmProject()

    def run_tests(self, args):
        print "for '{}'...{}".format(args.project, PYBRAT_SHGRAY)
        if not args.brew:
            pre_venv_d = get_venv_dict({'pybrat':args.project})
        testout = self.run_subcmd(args)
        if args.verbose > 1:
            print testout.getvalue()
        if args.brew:
            if args.project not in get_venv_dict({'brew':True}).keys():
                if args.verbose:
                    print "==> '{}' removed.".format(args.project)
                return True
            else:
                return False
        post_venv_d = get_venv_dict({'pybrat':args.project})
        for vname in pre_venv_d.keys():
            if vname not in post_venv_d.keys():
                if args.verbose:
                    print "==> '{}' removed.".format(vname)
            else:
                return False
        if args.project in get_project_list({'pybrat':True}).keys():
            return False
        return True
  

class UseTest(PybratTest):
    name = 'use'

    def __init__(self):
        super(UseTest, self).__init__()
        from pybrat.subcommands.use import UseProject
        self.subcmd = UseProject()

    def run_tests(self, args):
        print "UseTest: ", self.subcmd
        print "Args: ", args
        return False


### Checkup command class ###

class Checkup(Subcommand):
    name = "checkup"
    description = "Run subcommand tests (For now just one. Later cleanup tools, too.)"
    help = "testbench utilities and cleanup tools"
    # extra testy stuff
    tests = {}
    test_dir = '/tmp/pybrat_testzone'

    def __init__(self):
        super(Checkup, self).__init__()
        self.parser.add_argument("number", type=int, choices=[1],
                                 help="checkup choice")
        self.parser.add_argument("--verbose", type=int, choices=[0,1,2],
                                 help="feedback level during tests")
        self.parser.set_defaults(command=self)

    def _instant_tests(self):
        self.tests['list'] = ListTest()
        self.tests['init'] = InitTest()
        self.tests['mk'] = MkTest()
        self.tests['rm'] = RmTest()
        self.tests['use'] = UseTest()

    def run_command(self, args):
        self._instant_tests()
        old_dir = self._chdir_testdir()
        results = {}
        if args.number == 1:
            results['checkup01'] = self._run_checkup01(args)
        self._chdir_testdir(old_dir=old_dir)
        self._print_results(args, results)

    def _chdir_testdir(self, old_dir=""):
        if not old_dir:
            old_dir = os.getcwd()
            print "Changing to pybrat test dir '{}'...".format(self.test_dir)
            pv_mkdirs(self.test_dir)
            os.chdir(self.test_dir)
            return old_dir
        else:
            print "Changing back to your dir '{}'...".format(old_dir)
            os.chdir(old_dir)
            shutil.rmtree(self.test_dir)
            return None

    def _print_results(self, args, results):
        for checkup, result in results.iteritems():
            print "\n{}{}:".format(PYBRAT_SHGREEN, checkup)
            for test in result:
                for tname, tres in test.iteritems():
                    print "%s%12s: " % (PYBRAT_SHGRAY, tname),
                    if tres:
                        print "{}{}".format(PYBRAT_SHGREEN, tres)
                    else:
                        print "{}{}".format(PYBRAT_SHRED, tres)

    def _run_checkup01(self, args):
        result = []
        args = {'project':"pybrat_checkup01", 'python':"2.7", 'brew':False,
                'wrap':False, 'venv':False, 'verbose':args.verbose}
        # make a project and pybrew venv (check it worked)
        result.append( {'mk01': self.tests['mk'].run(args, outcome=True)} )
        # list pybrat projects (check new proj is in it)
        result.append( {'list01': self.tests['list'].run(args, outcome=True)} )
        # rm the proj but not the venv (check it worked)
        result.append( {'rm01': self.tests['rm'].run(args, outcome=True)} )
        # list (1) pybrat projs (2) pybrew (gone from (1), still in (2))
        result.append( {'list02': self.tests['list'].run(args, outcome=False)} )
        args['brew'] = True
        result.append( {'list03': self.tests['list'].run(args, outcome=True)} )
        # rm the venv too
        result.append( {'rm02': self.tests['rm'].run(args, outcome=True)} )
        # should be gone from list -b
        result.append( {'list04': self.tests['list'].run(args, outcome=False)} )
        # mk a venv only
        result.append( {'mk02': self.tests['mk'].run(args, outcome=True)} )
        # init the still-existing proj dir from mk01 with venv from mk02
        args['virtualenv'] = args['project']
        result.append( {'init01': self.tests['init'].run(args, outcome=True)} )
        args['brew'] = False
        result.append( {'list05': self.tests['list'].run(args, outcome=True)} )
        # rm it for good
        args['venv'] = True
        result.append( {'rm03': self.tests['rm'].run(args, outcome=True)} )
        args['venv'] = False
        result.append( {'list06': self.tests['list'].run(args, outcome=False)} )

        return result
                      

# instantiate
Checkup()
