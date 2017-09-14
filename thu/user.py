"""User
Load and store userinfo.

Default save user info(username and password) at ~/.thu

Author: Yeoman
Date: 2017-09-02
"""

import os
import os.path
import pickle
import getpass

__all__ = ['getuser', 'setuser', 'show']

home_dir = os.path.expanduser('~')
filename = os.path.join(home_dir, '.thu')


def _load(path=filename):
    if not os.path.exists(path):
        setuser()
    with open(path, 'rb') as f:
        return pickle.load(f)


def _store(data, path=filename):
    with open(path, 'wb') as f:
        pickle.dump(data, f)
    os.chmod(path, 0o600)


def setuser():
    """ Create new user """
    username = input('Username: ').encode()
    password = getpass.getpass().encode()
    data = {}
    data['username'] = username
    data['password'] = password
    _store(data)


def getuser():
    """ Get user info """

    return _load()


def show():
    """ Show username """
    print(_load()['username'].decode())


main = show
