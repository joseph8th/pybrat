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

This version of `pybrat` requires the following:

    * python2.7
    * pyenv
    * pythonbrew (deprecated)
    * virtualenv
    * virtualenvwrapper

Installation
------------

It is **strongly advised** that you use the `install` shell (bash) script to install, uninstall or upgrade `pybrat`.
There may be future updates to the structure and contents of the project link directory, which `install` will make
before updating `pybrat` source files.

Before installing `pybrat`, the interactive `install` script checks dependencies, and will prompt the user to install
and configure each them in default locations. If dependencies are already met, you can still use the `-i` option to 
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

    {list,init,mk,rm,use}

    ls      List all pybrat projects (optional: list virtualenvs).

        optional arguments:
          -b, --brew            list pythonbrew virtualenvs
          -w, --wrap            list virtualenvwrapper virtualenvs
          -v VENV, --venv VENV  find wild virtualenvs on VENV (path)

    init    Create new pybrat project link from given project dir and venv. 
        Flags '-w' or '-v' will import 'virtualenv' to a new pythonbrew venv.

        positional arguments:
          project     your existing project directory
          virtualenv  your existing pythonbrew virtualenv (import with flags)

        optional arguments:
          -w, --wrap  virtualenvwrapper venv NAME (not path)
          -v, --venv  wild virtualenv PATH (rel. or abs.)

    mk      Create and link new project directory and new pythonbrew venv.

        positional arguments:
          project     your new project directory and venv name
          python      X.Y[.Z] python version (in 'Python-X.Y.Z')

        optional arguments:
          -b, --brew  create a pythonbrew venv but no project

    rm      Remove pybrat project (leaves your project directory alone).

        positional arguments:
          project     pybrat project or pybrew venv to remove (mod with flags)

        optional arguments:
          -v, --venv  ALSO delete any venvs linked to 'project'
          -b, --brew  ONLY delete pythonbrew venv named 'project'

    use     Use pybrat project (venv and/or python) in a subshell.

        positional arguments:
          project           use given pybrat project (unless '-p' flag set)

        optional arguments:
          -v VENV, --venv VENV  use virtualenv 'VENV' (if multi-venv project)
          -p, --python          ONLY use given python version (X.Y[.Z])

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

    0.0 - basic functionality hacked out in a pile of sleepless sloppy code
    0.1 - changed name from 'pyvenv' (taken) to 'pybrat
    0.2 -  added support for 'pyenv' python/virtualenv manager

Author
------

    Written by Joseph Edwards VIII (joseph8th@notroot.us)