# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with io.open("samplemod/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='samplemod',
    version=version,
    description='TODO',
    long_description=readme,
    author='Duino Du',
    author_email='duino472365351@gmail.com',
    url='https://github.com/duinodu/samplemod',
    license=license,
    packages=find_packages("samplemod")
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=[],
    entry_points={"console_scripts": ["samplemod = samplemod.cli:main"]},
)
