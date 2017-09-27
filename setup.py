from distutils.core import setup
from distutils.extension import Extension
#import os
#import sysconfig

# Common flags for both release and debug builds.
#extra_compile_arguments = sysconfig.get_config_var('CFLAGS').split()
extra_compile_arguments = ["-std=c++11", "-O3","-Wall", "-Wextra","-xc++"]
extra_link_arguments    = ["-Wl,--no-undefined","-lstdc++","-shared-libgcc","-Wl,-rpath,$(pwd)"]

setup(
    name                = 'PolyominoModel',
    version             = '0.2.0',
    author              = 'AS Leonard',
    packages            = ['polyominomodel'],
    author_email        = 'asl47@cam.ac.uk',
    description         = 'Various polyomino fun parts',
    long_description    = open('README.txt').read(),
    license             = 'LICENSE.txt',
    ext_modules         = [Extension("polyominomodel.CLAM",sources=['src/tile_methods.cpp','src/tile_analysis.cpp','src/polyomino_wrapper.cpp'],include_dirs = ['src/includes'],extra_compile_args=extra_compile_arguments,extra_link_args=extra_link_arguments,language='c++11')],
    headers             = ['src/includes/tile_analysis.hpp','src/includes/tile_methods.hpp','src/includes/xorshift.hpp']
    )
