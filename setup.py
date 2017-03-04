#
# encoding=utf8

from setuptools import setup

setup(name="thu",
      version="1.0.2",
      description="Login,logout,check tsinghua net",
      author="zyeoman",
      author_email="zyeoman@163.com",
      url="https://github.com/zyeoman/thu",
      packages=['thu'],
      install_requires=[
          'bs4',
          'prettytable',
      ],
      scripts=['scripts/thu', 'scripts/thu.bat']
      )
