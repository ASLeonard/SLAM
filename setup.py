import sys
import os
from setuptools.command.test import test as TestCommand
from distutils.core import setup
from distutils.extension import Extension



# Common flags for both release and debug builds.
#extra_compile_arguments = sysconfig.get_config_var('CFLAGS').split()

extra_compile_arguments = ["-std=c++11", "-O3","-Wall", "-Wextra","-xc++"]
extra_link_arguments    = ["-Wl,-undefined,error","-lstdc++","-shared-libgcc"]


here = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(here, 'polyominomodel/version.py')).read())



class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)
	

setup(
    name                = 'PolyominoModel',
    version             = __version__,
    author              = 'AS Leonard',
    packages            = ['polyominomodel'],
    tests_require       = ['pytest'],
    cmdclass            = {'test': PyTest},
    author_email        = 'asl47@cam.ac.uk',
    description         = 'Various polyomino fun parts',
    long_description    = open('README.md').read(),
    license             = 'LICENSE.txt',
    platforms           = ["posix"],
    url                 = "https://github.com/IcyHawaiian/SLAM",
    ext_modules         = [Extension("polyominomodel.CLAM",sources=['src/graph_methods.cpp','src/graph_analysis.cpp','src/polyomino_wrapper.cpp'],include_dirs = ['src/includes'],extra_compile_args=extra_compile_arguments,extra_link_args=extra_link_arguments,language='c++11')],
    headers             = ['src/includes/graph_analysis.hpp','src/includes/graph_methods.hpp','src/includes/xorshift.hpp']
)
