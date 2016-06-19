#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

from _version import __version__
from _name import __appname__
from rds_snapshot_restore import __author__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requires = ['boto3>=1.2']

setup(
    name=__appname__,
    version=__version__,
    description='Fast restore most current snapshot to new rds-instance',
    long_description=long_description,
    url='https://github.com/truffls/rds_shapshot_restore',
    author=__author__,
    author_email='mail@johannesreichard.de',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='aws rds development database snapshot',
    py_modules=["rds_snapshot_restore"],
    install_requires=requires,

    entry_points={
        'console_scripts': [
            'rds_snapshot_restore=rds_snapshot_restore:main',
        ],
    },
)
