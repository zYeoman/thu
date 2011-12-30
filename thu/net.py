__all__ = ['check', 'login', 'logout', 'main']

from urllib.request import urlopen, Request
from urllib.parse import urlencode
from hashlib import md5
from collections import namedtuple

from .user import username, password

NetUsage = namedtuple('NetUsage', 'id user traffic unknown timelen')

def check():
    req = Request('http://net.tsinghua.edu.cn/cgi-bin/do_login', b'action=check_online')
    resp = urlopen(req).read().decode()
    info = NetUsage(*resp.split(','))
    print(info)

def login():
    data = urlencode({
        'username': username,
        'password': md5(password).hexdigest(),
        'drop': 0,
        'type': 1,
        'n': 100
        })
    req = Request('http://net.tsinghua.edu.cn/cgi-bin/do_login', data.encode())
    resp = urlopen(req).read().decode()
    print(resp)
    check()

def logout():
    req = Request('http://net.tsinghua.edu.cn/cgi-bin/do_logout', b'')
    print(urlopen(req).read().decode())

main = check
