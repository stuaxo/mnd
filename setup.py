from glob import glob
from os.path import abspath, basename, dirname, join, normpath, relpath
from shutil import rmtree

from setuptools import setup, find_packages
from setuptools import Command

VERSION="0.2.1"
long_description="""
Match 'n Dispatch


Match python args and dispatch based on their contents.


Getting started

Create a dispatcher


from mnd.dispatch import Dispatcher, handle
d = Dispatcher()


Use the handy decorator
>>> @handler(d, msg="hello")
>>> def say(msg=None):
...     print "got message: ", msg


Try dispatching some events
```python
>>> d.dispatch(msg="gets filtered out..."))
>>> d.dispatch(msg="hello"))
got message: hello


Install

$ pip install mnd
"""

here = normpath(abspath(dirname(__file__)))
class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    CLEAN_FILES = './build ./dist ./*.pyc ./*.tgz ./*.egg-info ./__pycache__'.split(' ')

    user_options = []

    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        global here

        for path_spec in self.CLEAN_FILES:
            # Make paths absolute and relative to this path
            abs_paths = glob(normpath(join(here, path_spec)))
            for path in [str(p) for p in abs_paths]:
                if not path.startswith(here):
                    # Die if path in CLEAN_FILES is absolute + outside this directory
                    raise ValueError("%s is not a path inside %s" % (path, here))
                print('removing %s' % relpath(path))
                rmtree(path)


setup(
    name='mnd',

    cmdclass={
        'clean': CleanCommand,
    },
    test_suite = 'tests',
    tests_require = ["six"],

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=VERSION,

    description='Match python args and dispatch based on their contents.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/stuaxo/mnd',

    # Author details
    author='Stuart Axon',
    author_email='stuaxo2@yahoo.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='match dispatch',

    packages=["mnd"],

)
