PyBrat
======

pybrat - python project manager and pythonbrew commander

The Wannabe-Ultimate Pythonbrew Commander and Virtualenv Wrangler.
Manage your python projects' source directories, python versions and
pythonbrew virtualenvs. Command pythonbrew using your pybrat project.
Intended to centralize and simplify common pythonic activities.

Usage
-----

    pybrat [OPTION] {COMMAND} [OPTION]... [ARGS]...

Installation
------------

    $ git clone git@github.com:joseph8th/pybrat.git

    $ cd ./pybrat

    $ ./pybrat-install

To uninstall or reinstall, use the `-u` or `-r` options. See `-h` for `--help`.

Commands
--------

    {list,init,mk,rm,use}

    list    List all pybrat projects (optional: list virtualenvs).

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

    * Uses deprecated os.system call to create the subshell.
    * Doesn't really communicate with pythonbrew in subprocess calls.

Changelog
---------

    0.0 - basic functionality hacked out in a pile of sleepless sloppy code
    0.1 - changed name from 'pyvenv' (taken) to 'pybrat'

Author
------

    Written by Joseph Edwards VIII (joseph8th@notroot.us)