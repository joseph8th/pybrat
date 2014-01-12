#!/usr/bin/env python

import os
from distutils.core import setup

from pybrat.define import PYBRAT_VER, PYBRAT_PROG_DESCRIPTION

README = os.path.join(os.path.dirname(__file__),'PKG-INFO')
#LONG_DESCRIPTION = open(README).read() + "\n"

setup(
    name='pybrat',
    version=PYBRAT_VER,
    packages=['pybrat', 'pybrat.subcommands', 'pybrat.hacks',],
    scripts=['install', 'pybrat.py',],
    data_files=[ ('', ['etc/bashrc', 'etc/pybrat.cfg']),
                 ('hacks', []),
                 ('hooks', ['etc/hooks/preactivate.skel', 
                            'etc/hooks/postactivate.skel',
                            'etc/hooks/predeactivate.skel', 
                            'etc/hooks/postdeactivate.skel']),
                 ],

    keywords='python',
    description=PYBRAT_PROG_DESCRIPTION,
#    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Free for non-commercial use',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python',
        ],

    author='Joseph Edwards VIII',
    author_email='joseph8th@notroot.us',

    #      url='http://urcomics.com/git/?p=pybrat.git;a=summary',
    #      license='MIT',
    #      entry_points=dict(console_scripts=['pythonbrew_install=pythonbrew.installer:install_pythonbrew']),
    #      test_suite='nose.collector',
    #      tests_require=['nose'],
    #      zip_safe=False
    )
