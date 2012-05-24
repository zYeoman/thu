#!/usr/bin/python3
#encoding: utf8

from http.cookiejar import CookieJar
from urllib.request import Request, HTTPCookieProcessor, build_opener
from urllib.parse import urlencode
from hashlib import md5
from collections import namedtuple
from bs4 import BeautifulSoup

from .user import username, password

BASE_URL = 'https://usereg.tsinghua.edu.cn/'

IpInfo = namedtuple('IpInfo', 'user ip usage_in usage_out balance credit client login_time avail_usage avail_time checksum')

class Usereg:
    def __init__(self, username, password):
        cj = CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(cj))
        self.login(username, password)

    def login(self, username, password):
        self.username = username
        self.password = md5(password).hexdigest()
        url = BASE_URL + 'do.php'
        data = dict(
                action = 'login',
                user_login_name = username,
                user_password = self.password
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
        data = dict(action = 'logout')
        req = Request(url, urlencode(data).encode('utf8'))
        resp = self.opener.open(req)
        content = resp.read().decode('gbk')
        if content != 'ok':
            raise Exception(content)

    def iplist(self):
        url = BASE_URL + 'online_user_ipv4.php'
        content = self.opener.open(url).read().decode('gbk')
        tree = BeautifulSoup(content)
        rows = tree.body.table.find_all('table')[1].find_all('tr')
        for row in rows[1:]:
            values = [x.string.strip() for x in row.find_all('td') if x.string][1:]
            values.append(row.input.attrs['onclick'].split('\'')[3])
            yield IpInfo(*values)

    def ipup(self, ip):
        url = 'http://166.111.8.120/cgi-bin/do_login'
        values = dict(
                n = 100,
                is_pad = 1,
                type = 10,
                username = self.username,
                password = self.password,
                user_ip = ip
                )
        req = self.opener.open(url, urlencode(values).encode('utf8'))
        content = req.read().decode('utf8')
        if content != '登录成功':
            raise Exception(content)
        else:
            return 'ok'

    def ipdown(self, ip):
        url = BASE_URL + 'online_user_ipv4.php'
        index = None
        checksum = None

        try:
            index = int(ip)
            ipr = list(self.iplist())[index]
            ip = ipr.ip
            checksum = ipr.checksum
        except Exception as e:
            pass

        if not checksum:
            for i in self.iplist():
                if i.ip == ip:
                    checksum = i.checksum

        if not checksum:
            raise Exception('ip not found')

        values = dict(
                action = 'drop',
                user_ip = ip,
                checksum = checksum,
                )
        req = self.opener.open(url, urlencode(values).encode('utf8'))
        content = req.read().decode('utf8')
        if content != 'ok':
            raise Exception(content)
        return content


def iplist():
    u = Usereg(username, password)
    for i in u.iplist():
        print(i)
    u.logout()

def ipup(ip):
    u = Usereg(username, password)
    print(u.ipup(ip))
    u.logout()

def ipdown(ip):
    u = Usereg(username, password)
    print(u.ipdown(ip))
    u.logout()

def ipcheckup(ip):
    u = Usereg(username, password)
    for i in u.iplist():
        if i.ip == ip:
            print('already online')
            break
    else:
        u.ipup(ip)

main = iplist
