#!/usr/bin/python3
# encoding: utf8

from http.cookiejar import CookieJar
from urllib.request import Request
from urllib.request import HTTPCookieProcessor, build_opener, HTTPSHandler
from urllib.parse import urlencode
from hashlib import md5
from bs4 import BeautifulSoup
from prettytable import PrettyTable

import ssl

from .user import username, password

BASE_URL = 'https://usereg.tsinghua.edu.cn/'


class Usereg:

    def __init__(self, username, password):
        cj = CookieJar()
        self.gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.opener = build_opener(HTTPCookieProcessor(
            cj), HTTPSHandler(context=self.gcontext))
        self.login(username, password)

    def login(self, username, password):
        self.username = username
        self.password = md5(password).hexdigest()
        url = BASE_URL + 'do.php'
        data = dict(
            action='login',
            user_login_name=username,
            user_password=self.password
        )
        req = Request(url, urlencode(data).encode('utf8'))
        resp = self.opener.open(req)
        content = resp.read().decode('gbk')
        if content != 'ok':
            raise Exception(content)

    def logout(self):
        self.username = None
        self.password = None
        url = BASE_URL + 'do.php'
        data = dict(action='logout')
        req = Request(url, urlencode(data).encode('utf8'))
        resp = self.opener.open(req)
        content = resp.read().decode('gbk')
        if content != 'ok':
            raise Exception(content)

    def iplist(self):
        url = BASE_URL + 'online_user_ipv4.php'
        content = self.opener.open(url).read().decode('gbk')
        tree = BeautifulSoup(content, 'html.parser')
        rows = tree.body.table.find_all('table')[1].find_all('tr')
        for row in rows:
            values = [x.string.strip() for x in row.find_all('td') if x.string]
            yield values

    def ipdown(self, ip):
        url = BASE_URL + 'online_user_ipv4.php'
        index = None

        if ip.isdigit():
            index = int(ip)
            ipr = list(self.iplist())[index]
            ip = ipr[0]

        values = dict(
            action='drop',
            user_ip=ip
        )
        req = self.opener.open(url, urlencode(values).encode('utf8'))
        content = req.read().decode('gbk')
        return content

    def ipup(self, ip):
        url = BASE_URL + 'ip_login.php'
        values = dict(
                n = 100,
                is_pad = 1,
                type = 10,
                action = 'do_login',
                user_ip = ip,
                drop = 0
                )
        req = self.opener.open(url, urlencode(values).encode('utf8'))
        content = req.read().decode('gbk')
        return 'ok'


def iplist():
    u = Usereg(username, password)
    for _, i in enumerate(u.iplist()):
        i = i[0:4] + i[-6:]
        if _ == 0:
            t = PrettyTable(i)
        else:
            t.add_row(i)
    print(t)
    u.logout()


def ipdown(ip):
    u = Usereg(username, password)
    print(u.ipdown(ip))
    u.logout()

def ipup(ip):
    u = Usereg(username, password)
    print(u.ipup(ip))
    u.logout()

main = iplist
