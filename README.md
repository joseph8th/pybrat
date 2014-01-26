PyBrat
======

pybrat - python project manager with virtualenv support

Manage your python projects' source directories, python versions and pythonbrew virtualenvs using one command.
Manage your linked source code projects using pythonbrew (deprecated), pyenv, virtualenv and/or virtualenvwrapper. 

Usage
-----

    pybrat [OPTION] {COMMAND} [OPTION]... [ARGS]...

Dependencies
------------

### Required:

    * 'pyenv' - with Python-2.7.6)
    * 'pyenv-virtualenv' - 'pyenv' plugin

### Optional:

    * pythonbrew (deprecated)
    * virtualenv
    * virtualenvwrapper

Installation
------------

It is **strongly advised** that you use the `install` shell (bash) script to install, uninstall or upgrade `pybrat`.
There may be future updates to the structure and contents of the project link directory, which `install` will make
before updating `pybrat` source files.

Before installing `pybrat`, the interactive `install` script checks dependencies, and will prompt the user to install
and configure each in default locations. If dependencies are already met, you can still use the `-i` option to 
install and check configuration.

    $ git clone git@github.com:joseph8th/pybrat.git ~/.pybrat

    $ cd ~/.pybrat

    $ ./install -i

Use the `-u` or `-r` options to uninstall or reinstall, respectively. 

Use the `-d` option to uninstall *and* delete the user project *links* directory 
(does **not** touch original project source files).

Use `-h` for `--help`.

Usage
-----

    $ pybrat {ls, init, mk, rm, use}

Commands
--------

    {ls,init,mk,rm,use,fix,sync}

    ls      List all pybrat projects, virtualenvs or pythons.

        optional arguments:
          -v, --venv    list ONLY known virtualenvs
          -p, --python  list ALL known python versions

    init    Create new pybrat project link from given project dir and virtualenv. 

        positional arguments:
          project     root of your existing source code directory
          virtualenv  your existing known virtualenv

        optional arguments:
          -v, --venv  import 'virtualenv' into 'project' from known virtualenvs

    mk      Create and link new project directory and new virtualenv.

        positional arguments:
          project     your new project directory and venv name
          python      X.Y.Z python version (in 'Python-X.Y.Z')

        optional arguments:
          -v, --venv  create a virtualenv but no project

    rm      Remove pybrat project (leaves source code alone).

        positional arguments:
          name        name of pybrat project (or virtualenv to remove)

        optional arguments:
          -a, --all   ALSO delete any venvs linked to project 'name'
          -v, --venv  ONLY delete linked virtualenv 'name'

    use     Use pybrat project, virtualenv or python.

        positional arguments:
          name                  use given pybrat project, virtualenv or python

        optional arguments:
          -v VENV, --venv VENV  use virtualenv 'name' (multi-venv project)
          -p, --python          use given python version X.Y.Z

Examples
--------

    To list all your pybrat projects and linked virtualenvs, use:

        $ pybrat list

    To initialize an existing 'myproject' directory using an imported 'wild' virtualenv:

        $ pybrat init -v myproject ./path/to/venv

    To use a selected venv in a multi-venv project:

        $ pybrat use myproject -v myvenv

Known Bugs
----------

    * Uses deprecated os.system call to create the subshell for pythonbrew.
    * Doesn't really communicate with pythonbrew in subprocess calls.

Changelog
---------

    0.2 -  * Added support for 'pyenv' python/virtualenv managers.
           * Refactored shell script 'pybrat-install' --> 'install'.
           * Moved installation into 'install' script; removed python installer to allow booting. 
           * Refactored package structure to suit 'distutils' with 'setup.cfg'.
           * Moved 'hacks' code (pyenv, brew, wrap, etc) into their own scripts/modules, with an
             eye on a future plugin API.
           * Reduced 'define.py' by 'etc/pybrat.cfg' default install config, and DRYness refactor.
           * Added features to 'install' script: 
             - interactive modular dependencies install-to-default using latest stable releases
               and latest recommended install methods;
             - bootstraps most stable Python version for current version of 'pybrat' and
               installs 'pybrat' into a 'pyenv virtualenv' for future feature portability;
             - offers to install and/or configure optional dependencies like 'pythonbrew' and
               'virtualenvwrapper' for use by included 'hacks' (not quite 'plugins', yet);
             - simplifies installation, uninstallation, deletion, and updating (via git).

    0.1 -  changed name from 'pyvenv' (taken) to 'pybrat'

    0.0 -  basic functionality hacked out in a pile of sleepless sloppy code


Author
------

    Written by Joseph Edwards VIII (joseph8th@notroot.us)