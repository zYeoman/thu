#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Setupfile
'''

import os
from setuptools import setup

NAME = 'thu'
DESCRIPTION = 'Tool for login/logout tsinghua network'
URL = 'https://github.com/zYeoman/thu'
EMAIL = 'zyeoman@163.com'
AUTHOR = 'Yongwen Zhuang'

REQUIRED = [
    'requests',
    'bs4',
    'prettytable'
]

HERE = os.path.abspath(os.path.dirname(__file__))

with open('README.md', 'rb') as f:
    LONG_DESCRIPTION = f.read().decode('utf-8')


with open('thu/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

setup(
    name="thu",
    version=version,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=['thu'],
    install_requires=REQUIRED,
    scripts=['scripts/thu', 'scripts/thu.bat']
)
