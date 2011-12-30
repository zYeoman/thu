from urllib.request import urlopen, Request
from urllib.parse import urlencode
from hashlib import md5

from .user import username, password

def login():
    url = 'http://wireless.tsinghua.edu.cn/cgi-bin/cisco_auth'
    data = urlencode({
        'action': b'login',
        'username': username,
        'password': md5(password).hexdigest(),
        'vip': 13
        })
    req = Request(url, data.encode())
    print(urlopen(req).read())

main = login
