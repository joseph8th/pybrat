import os
from setuptools import setup, find_packages
from pybrat.define import PYBRAT_VER

README = os.path.join(os.path.dirname(__file__),'PKG-INFO')
long_description = open(README).read() + "\n"

setup(name='pybrat',
      version=PYBRAT_VER,
      description="Wannabe pythonbrew commander and virtualenv wrangler.",
      long_description=long_description,
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Free for non-commercial use',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python',
      ],
      keywords='pythonbrew virtualenv virtualenvwrapper',
      author='Joseph8th',
      author_email='joseph8th@urcomics.com',
#      url='http://urcomics.com/git/?p=pybrat.git;a=summary',
#      license='MIT',
      packages=find_packages(),
      include_package_data=True,
#      entry_points=dict(console_scripts=['pythonbrew_install=pythonbrew.installer:install_pythonbrew']),
#      test_suite='nose.collector',
#      tests_require=['nose'],
#      zip_safe=False
)
