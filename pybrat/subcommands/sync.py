from pybrat.subcommand import Subcommand

class SyncProject(Subcommand):
    name = "sync"
    description = "Sync your project with a remote version repository or source directory."
    help = "sync pybrat project with remote version system"

    def __init__(self):
        super(SyncProject, self).__init__()
        self.parser.add_argument('project', help="name of pybrat project to sync")
        self.parser.add_argument('repo', choices=('git', 'fabric', 'rsync',), 
                                 default='git', help="type of sync engine to use")
        self.arg_group = self.parser.add_mutually_exclusive_group()
        self.arg_group.add_argument(
            '-c', '--commit', action="store",
            help="commit changes using chosen repo, with message COMMIT")
        self.arg_group.add_argument(
            '-r', '--remote', action="store",
            help="set remote repo with which to sync")
        self.arg_group.set_defaults(command=self)

    def run_command(self, args):
        pass


SyncProject()
