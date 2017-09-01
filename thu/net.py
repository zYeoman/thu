"""
net.py
Communicate with net.tsinghua.edu.cn.

Author: Yeoman
Date: 2017-09-02
"""
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from hashlib import md5

__all__ = ['check', 'login', 'logout', 'main']


def check():
    """ Check if online. If so, show usage info. """
    req = Request('http://net.tsinghua.edu.cn/do_login.php',
                  b'action=check_online')
    resp = urlopen(req).read().decode()
    print(resp)
    if resp != 'not_online':
        req = Request('http://net.tsinghua.edu.cn/rad_user_info.php', b'')
        resp = urlopen(req).read().decode()
        info = resp.split(',')
        traffic = int(info[6]) / 1000000000
        timelen = int(info[2]) - int(info[1])
        timelen_str = '{}:{}:{}'.format(
            timelen // 3600,
            timelen // 60 % 60,
            timelen % 60)
        info_s = 'ip={0[8]},user={0[0]},traffic={1:.2f}GB,timelen={2}'
        info_s = info_s.format(info, traffic, timelen_str)
        print(info_s)


def login():
    """ Login to net.tsinghua.edu.cn """
    from .user import username, password
    from .user import setuser

    data = urlencode({
        'action': 'login',
        'username': username,
        'password': '{MD5_HEX}' + md5(password).hexdigest(),
        'ac_id': 1
    })
    req = Request('http://net.tsinghua.edu.cn/do_login.php', data.encode())
    resp = urlopen(req).read().decode()
    print(resp)
    if resp.startswith('E'):
        setuser()
    check()


def logout():
    """ Logout from net.tsinghua.edu.cn """
    date = urlencode({
        'action': 'logout'
    })
    req = Request('http://net.tsinghua.edu.cn/do_login.php', date.encode())
    print(urlopen(req).read().decode())


main = check
