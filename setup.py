# encoding=utf8
'''
Setupfile
'''

from setuptools import setup

with open('README.md', 'rb') as f:
    README = f.read().decode('utf-8')

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
    description=README,
    author="zyeoman",
    author_email="zyeoman@163.com",
    url="https://github.com/zyeoman/thu",
    packages=['thu'],
    install_requires=[
        'requests',
        'bs4',
        'prettytable',
    ],
    scripts=['scripts/thu', 'scripts/thu.bat']
)
