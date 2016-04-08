
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from hashlib import md5
from collections import namedtuple

from .user import username, password

__all__ = ['check', 'login', 'logout', 'main']

NetUsage = namedtuple('NetUsage', 'ip user traffic timelen')


def check():
    req = Request('http://net.tsinghua.edu.cn/do_login.php',
                  b'action=check_online')
    resp = urlopen(req).read().decode()
    print(resp)
    if resp != 'not_online':
        req = Request('http://net.tsinghua.edu.cn/rad_user_info.php', b'')
        resp = urlopen(req).read().decode()
        info = resp.split(',')
        info = NetUsage(*[info[8], info[0], int(info[6]) /
                          1000000000, int(info[2]) - int(info[1])])
        print(info)


def login():
    data = urlencode({
        'action': 'login',
        'username': username,
        'password': '{MD5_HEX}' + md5(password).hexdigest(),
        'ac_id': 1
    })
    req = Request('http://net.tsinghua.edu.cn/do_login.php', data.encode())
    resp = urlopen(req).read().decode()
    print(resp)
    check()


def logout():
    date = urlencode({
        'action': 'logout'
    })
    req = Request('http://net.tsinghua.edu.cn/do_login.php', date.encode())
    print(urlopen(req).read().decode())

main = check
