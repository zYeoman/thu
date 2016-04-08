import os
import os.path
import pickle
import getpass

if 'Home' in os.environ.keys():
    filename = os.path.join(os.environ[b'HOME'], b'.thu')
else:
    filename = os.path.join(os.environ['USERPROFILE'], '_thu')


def _load(path=filename):
    with open(path, 'rb') as f:
        return pickle.load(f)


def _store(d, path=filename):
    with open(path, 'wb') as f:
        pickle.dump(d, f)
    os.chmod(path, 0o600)


def setuser():
    username = input('Username: ').encode()
    password = getpass.getpass().encode()
    d = {}
    d['username'] = username
    d['password'] = password
    _store(d)


def show():
    print(_load())


def main():
    print(_load()['username'].decode())

try:
    _data = _load()
except Exception as e:
    print(e)
    setuser()
    _data = _load()

username = _data['username']
password = _data['password']
