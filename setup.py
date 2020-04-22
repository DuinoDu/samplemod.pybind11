# -*- coding: utf-8 -*-

import os
import sys
import io
import re
import setuptools
from setuptools import setup, find_packages
import setuptools.command.build_ext
import multiprocessing
from contextlib import contextmanager
from distutils.spawn import find_executable
from distutils import sysconfig, log
import shlex
import subprocess


TOP_DIR = os.path.realpath(os.path.dirname(__file__))
SRC_DIR = os.path.join(TOP_DIR, 'src/sample')
CMAKE_BUILD_DIR = os.path.join(TOP_DIR, '.setuptools-cmake-build')

CMAKE = find_executable('cmake3') or find_executable('cmake')
assert CMAKE, 'Could not find "cmake" executable!'


with open('README.md', 'r') as f:
    readme = f.read()

with open('LICENSE', 'r') as f:
    license = f.read()

with open('requirements.txt', 'r') as f:
    requires = []
    for line in f:
        line = line.strip()
        if not line.startswith('#'):
            requires.append(line)

with io.open("src/sample/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


@contextmanager
def cd(path):
    if not os.path.isabs(path):
        raise RuntimeError('Can only cd to absolute path, got: {}'.format(path))
    orig_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(orig_path)


class cmake_build(setuptools.Command):
    """
    Compile everything when `python setup.py build` is run using cmake.

    Custom args can be passed to cmake by specifying the `CMAKE_ARGS`
    environment variable.

    The number of CPUs used by `make` can be specified by passing `-j<ncpus>`
    to `setpy.py build`. By default all CPUs are used.
    """

    user_options = [
        (str('jobs='), str('j'), str('Specifies the number of jobs to use with make'))
    ]

    built = False
    
    def initialize_options(self):
        self.jobs = multiprocessing.cpu_count()

    def finalize_options(self):
        self.jobs = int(self.jobs)

    def run(self):
        if cmake_build.built:
            return
        cmake_build.built = True
        if not os.path.exists(CMAKE_BUILD_DIR):
            os.makedirs(CMAKE_BUILD_DIR)

        with cd(CMAKE_BUILD_DIR):
            build_type = 'Release'
            cmake_args = [
                CMAKE,
                f'-DPYTHON_INCLUDE_DIR={sysconfig.get_python_inc()}',
                f'-DPYTHON_EXECUTABLE={sys.executable}',
                f'-DCMAKE_EXPORT_COMPILE_COMMANDS=ON',
                '-DPY_EXT_SUFFIX={}'.format(sysconfig.get_config_var('EXT_SUFFIX') or ''),
            ]
            if 'CMAKE_ARGS' in os.environ:
                extra_cmake_args = shlex.split(os.environ['CMAKE_ARGS'])
                del os.environ['CMAKE_ARGS']
                log.info('Extra cmake args: {}'.format(extra_cmake_args))
                cmake_args.extend(extra_cmake_args)
            cmake_args.append(TOP_DIR)
            subprocess.check_call(cmake_args)

            build_args = [CMAKE, '--build', os.curdir]
            build_args.extend(['--', '-j', str(self.jobs)])
            subprocess.check_call(build_args)


class build_ext(setuptools.command.build_ext.build_ext):
    def run(self):
        self.run_command('cmake_build')
        setuptools.command.build_ext.build_ext.run(self)

    def build_extensions(self):
        for ext in self.extensions:
            fullname = self.get_ext_fullname(ext.name)
            filename = os.path.basename(self.get_ext_filename(fullname))
            lib_path = CMAKE_BUILD_DIR
            src = os.path.join(lib_path, filename)
            dst = os.path.join(os.path.realpath(self.build_lib), "sample", filename)
            self.copy_file(src, dst)
            # for py-unittest
            dst = os.path.join(os.path.realpath(TOP_DIR), "src/sample", filename)
            self.copy_file(src, dst)


cmdclass = {
    'cmake_build': cmake_build,
    'build_ext': build_ext,
}

ext_modules = [
    setuptools.Extension(
        name=str('sample.sample_cpp2py_export'),
        sources=[])
]

setup(
    name='sample',
    version=version,
    description='TODO',
    long_description=readme,
    author='user',
    author_email='duino472365351@gmail.com',
    url='https://github.com/user/sample',
    license=license,
    zip_safe=False,
    packages=find_packages("src"),
    package_dir={'': 'src'},
    include_package_data=True,
    cmdclass=cmdclass,
    ext_modules=ext_modules,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=requires,
    entry_points={"console_scripts": ["sample = sample.cli:main"]},
)
