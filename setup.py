# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='samplemod',
    version='0.1.0',
    description='TODO',
    long_description=readme,
    author='Duino Du',
    author_email='duino472365351@gmail.com',
    url='https://github.com/duinodu/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
