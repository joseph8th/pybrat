from pybrew.hacks.pyman import PythonManagerHack

class PythonbrewPythonMgr(PythonManagerHack):

    name = 'brew'

    def __init__(self):
        super(PythonMgr, self).__init__()

    def get_python_path(self, args):
        pass

    def get_python_list(self, args):
        pass

    def use_python(self, args):
        pass

    def install_python(self, args):
        pass

    def run_command(self, args):
        pass


# instantiate
PythonbrewPythonMgr()
