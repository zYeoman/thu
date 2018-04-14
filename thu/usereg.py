#!/usr/bin/python3
# encoding: utf8
"""Usereg
Info of usereg.tsinghua.edu.cn

  login: Login to usereg.tsinghua.edu.cn
  logout: Logout from usereg.tsinghua.edu.cn
  show: Show all online ip of usereg
  ipdown: Send logout to ip.

Author: Yeoman
Date: 2017-09-02
"""

import requests
from hashlib import md5
from bs4 import BeautifulSoup
from prettytable import PrettyTable

from .user import getuser


class Usereg():
    """Usereg for usereg.tsinghua.edu.cn"""

    def __init__(self):
        """init Usereg
        :param user: User info
        """
        self._session = requests.session()
        self._base = 'https://usereg.tsinghua.edu.cn/'
        self._login_url = self._base + 'do.php'

    def login(self):
        """login usereg.tsinghua.edu.cn
        :param user: User info
        :return: response text
        """
        user = getuser()
        data = {
            'action': 'login',
            'user_login_name': user['username'],
            'user_password': md5(user['password']).hexdigest(),
        }
        req = self._session.post(self._login_url, data)
        return req.text

    def logout(self):
        """logout usereg.tsinghua.edu.cn
        :return: response text
        """
        data = {'action': 'logout'}
        req = self._session.post(self._login_url, data)
        return req.text

    @property
    def iplist(self):
        """iplist of online ip
        :return: [] not login or iterator of ip info
        """
        url = self._base + 'online_user_ipv4.php'
        req = self._session.get(url)
        if req.text == '请登录先':
            return []
        tree = BeautifulSoup(req.content, 'html.parser')
        rows = tree.body.table.find_all('table')[1].find_all('tr')
        for row in rows:
            values = [x.string.strip() for x in row.find_all('td') if x.string]
            yield values

    def show(self):
        """show info of online ip
        :return: None
        """
        output = None
        for _, lst in enumerate(self.iplist):
            lst = lst[0:4] + lst[-6:]
            if _ == 0:
                output = PrettyTable(lst)
            else:
                output.add_row(lst)
        if output is None:
            print('请先登录')
        else:
            print(output)

    def ipdown(self, ip):
        """send logout request to usereg.tsinghua.edu.cn
        :param ip_str: str ip "127.0.0.1"
        :param index:  index of iplist
        :return: response text
        """
        url = self._base + 'online_user_ipv4.php'
        index = None

        if ip.isdigit():
            index = int(ip)
            ipr = list(self.iplist)[index]
            ip = ipr[0]

        values = {
            'action': 'drop',
            'user_ip': ip
        }
        req = self._session.post(url, values)
        return req.text

    def ipup(self, ip):
        url = self._base + 'ip_login.php'
        values = dict(
            n=100,
            is_pad=1,
            type=10,
            action='do_login',
            user_ip=ip,
            drop=0
        )
        self._session.post(url, values)
        return 'ok'


def iplist():
    u = Usereg()
    u.login()
    u.show()
    u.logout()


def ipdown(ip):
    u = Usereg()
    u.login()
    print(u.ipdown(ip))
    u.logout()


def ipup(ip):
    u = Usereg()
    u.login()
    print(u.ipup(ip))
    u.logout()


main = iplist
