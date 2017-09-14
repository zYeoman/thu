"""
net.py
Communicate with net.tsinghua.edu.cn.

Author: Yeoman
Date: 2017-09-13
"""
import requests
from hashlib import md5

__all__ = ['check', 'login', 'logout', 'main']


def check():
    """ Check if online. If so, show usage info. """
    req = requests.post('http://net.tsinghua.edu.cn/do_login.php',
                        {'action': 'check_online'})
    print(req.text)
    if req.text != 'not_online':
        req = requests.post('http://net.tsinghua.edu.cn/rad_user_info.php')
        info = req.text.split(',')
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
    from .user import getuser
    from .user import setuser

    user = getuser()
    data = {
        'action': 'login',
        'username': user['username'],
        'password': '{MD5_HEX}' + md5(user['password']).hexdigest(),
        'ac_id': 1
    }
    req = requests.post('http://net.tsinghua.edu.cn/do_login.php', data)
    print(req.text)
    if req.text.startswith('E'):
        setuser()
        login()
        return
    check()


def logout():
    """ Logout from net.tsinghua.edu.cn """
    date = {
        'action': 'logout'
    }
    req = requests.post('http://net.tsinghua.edu.cn/do_login.php', date)
    print(req.text)


main = check
