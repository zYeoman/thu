# -*- coding: utf-8 -*-
__author__ = 'kehao'
'''
[Origin](https://github.com/kehao95/thu_learn)

清华大学网络学堂爬虫
'''

import requests
from bs4 import BeautifulSoup, Comment
import re
import os
import logging
from user import password, username
from datetime import datetime

_DebugLevel = logging.DEBUG
logging.basicConfig(level=logging.DEBUG)

# global vars
_session = requests.session()
_URL_BASE_ = 'http://learn.tsinghua.edu.cn'
_URL_BASE = 'http://learn.tsinghua.edu.cn/MultiLanguage'
_URL_LOGIN = '/lesson/teacher/loginteacher.jsp'

# 学期
_URL_CURRENT_SEMESTER = '/lesson/student/MyCourse.jsp?typepage=1'
_URL_PAST_SEMESTER = '/lesson/student/MyCourse.jsp?typepage=2'
# 个人信息
_URL_PERSONAL_INFO = '/vspace/vspace_userinfo1.jsp'

# 课程不同板块前缀
# 课程公告
_PREF_MSG = '/public/bbs/getnoteid_student.jsp?course_id='
# 课程信息
_PREF_INFO = '/lesson/student/course_info.jsp?course_id='
# 课程文件
_PREF_FILES = '/lesson/student/download.jsp?course_id='
# 教学资源
_PREF_LIST = '/lesson/student/ware_list.jsp?course_id='
# 课程作业
_PREF_WORK = '/lesson/student/hom_wk_brw.jsp?course_id='


def login():
    """
    login to get cookies in _session
    :param user_id: your Tsinghua id "keh13" for example
    :param user_pass: your password
    :return:True if succeed
    """
    data = dict(
        userid=username,
        userpass=password,
    )
    r = _session.post(_URL_BASE + _URL_LOGIN, data)
    # 即使登录失败也是200所以根据返回内容简单区分了
    if len(r.content) > 120:
        logging.debug("login failed")
        return False
    else:
        logging.debug("login success")
        return True


def get_url(url):
    """
    _session.GET the page, handle the encoding and return the BeautifulSoup
    :param url: Page url
    :return: BeautifulSoup
    """
    r = _session.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


class Semester:
    """
    Class Semester have all courses in it
    """

    def __init__(self, current=True):
        """
        set the current flag to get current/past Semester
        :param current: Boolean True/False for Current/Past semester
        :return: None
        """
        login()
        if current:
            self.url = _URL_BASE + _URL_CURRENT_SEMESTER
        else:
            self.url = _URL_BASE + _URL_PAST_SEMESTER
        self._name = None

    @property
    def name(self):
        if not self._name:
            soup = get_url(self.url)
            self._name = soup.find('td', class_='active_on').text
        return self._name

    @property
    def courses(self):
        """
        return all the courses under the semester
        :return: Courses generator
        """
        soup = get_url(self.url)
        for j in soup.find_all('tr', class_=['info_tr', 'info_tr2']):
            i = j.find('a')
            url = i['href']
            if url.startswith('/Mult'):
                url = _URL_BASE_ + url
            else:
                # !!important!! ignore the new
                # WebLearning Courses At This moment
                continue
            nu = (int(x.contents[0])
                  for x in j.find_all('span', class_='red_text'))
            name = i.contents[0]
            name = re.sub(r'[\n\r\t ]', '', name)
            name = re.sub(r'\([^\(\)]+\)$', '', name)
            id = url[-6:]
            yield Course(name=name, url=url, id=id, nu=nu)


class Course:
    """
    this is the Course class
    """

    def __init__(self, id, url=None, name=None, nu=None):
        pass
        self._id = id
        self._url = url
        self._name = name
        self._nu = nu
        # self._works = list(self.works)
        # self._files = list(self.files)
        # self._messages = list(self.messages)
        # logging.debug(name)

    @property
    def url(self):
        """course url"""
        return self._url

    @property
    def name(self):
        """course name"""
        return self._name

    @property
    def id(self):
        """courses id"""
        return self._id

    @property
    def works(self):
        """
        get all the work in course
        :return: Work generator
        """
        url = _URL_BASE + _PREF_WORK + self._id
        soup = get_url(url)
        for i in soup.find_all('tr', class_=['tr1', 'tr2']):
            tds = i.find_all('td')
            if ("已经提交" in tds[3].contents[0]):
                continue
            url = _URL_BASE + '/lesson/student/' + \
                i.find('a')['href']
            id = re.search(r'(\d+)', url).group(0)
            title = i.find('a').contents[0].replace(u'\xa0', u' ')
            start_time = datetime.strptime(tds[1].contents[0], '%Y-%m-%d')
            end_time = tds[2].contents[0] + ' 23:59:59'
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            if end_time < datetime.now():
                continue
            yield Work(id=id, title=title,
                       url=url, start_time=start_time,
                       end_time=end_time)

    @property
    def all_works(self):
        """
        get all the work in course
        :return: Work generator
        """
        url = _URL_BASE + _PREF_WORK + self._id
        soup = get_url(url)
        for i in soup.find_all('tr', class_=['tr1', 'tr2']):
            tds = i.find_all('td')
            url = _URL_BASE + '/lesson/student/' + \
                i.find('a')['href']
            id = re.search(r'(\d+)', url).group(0)
            title = i.find('a').contents[0].replace(u'\xa0', u' ')
            start_time = datetime.strptime(tds[1].contents[0], '%Y-%m-%d')
            end_time = tds[2].contents[0] + ' 23:59:59'
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            yield Work(id=id, title=title,
                       url=url, start_time=start_time,
                       end_time=end_time)

    @property
    def messages(self):
        """
        get all messages in course
        :return: Message generator
        """
        url = _URL_BASE + _PREF_MSG + self.id
        soup = get_url(url)
        for m in soup.find_all('tr', class_=['tr1', 'tr2']):
            tds = m.find_all('td')
            if "已读" in tds[4].contents[0]:
                continue
            title = tds[1].contents[1].text.replace(u'\xa0', u' ')
            url = _URL_BASE + '/public/bbs/' + \
                tds[1].contents[1]['href']
            id = re.search(r"id=(\d+)", url).group(1)
            date = datetime.strptime(tds[3].text, '%Y-%m-%d')
            yield Message(title=title, url=url, date=date, id=id)
            # TODO

    @property
    def all_messages(self):
        """
        get all messages in course
        :return: Message generator
        """
        url = _URL_BASE + _PREF_MSG + self.id
        soup = get_url(url)
        for m in soup.find_all('tr', class_=['tr1', 'tr2']):
            tds = m.find_all('td')
            title = tds[1].contents[1].text.replace(u'\xa0', u' ')
            url = _URL_BASE + '/public/bbs/' + \
                tds[1].contents[1]['href']
            id = re.search(r"id=(\d+)", url).group(1)
            date = datetime.strptime(tds[3].text, '%Y-%m-%d')
            yield Message(title=title, url=url, date=date, id=id)
            # TODO

    @property
    def files(self):
        """
        get all files in course
        :return: File generator
        """

        def file_size_M(s):
            digitals = s[:-1]
            if s.endswith('K'):
                return float(digitals) / 1024
            elif s.endswith('M'):
                return float(digitals)
            else:
                return 1024 * float(digitals)

        url = _URL_BASE + _PREF_FILES + self.id
        soup = get_url(url)
        for j in soup.find_all('tr', class_=['tr1', 'tr2']):
            tds = j.find_all('td')
            if not tds[-1].contents:
                continue
            name = re.search(
                r'getfilelink=([^&]+)&',
                str(j.find(text=lambda text: isinstance(text,
                                                        Comment)))).group(1)
            url = 'http://learn.tsinghua.edu.cn/kejian/data/%s/download/%s' % (
                self.id, name)
            name = re.sub(r'_[^_]+\.', '.', name)
            size = file_size_M(tds[-3].text)
            title = tds[-5].a.text.strip() + name[-4:]
            yield File(size=size, name=name, url=url, title=title)

    @property
    def all_files(self):
        """
        get all files in course
        :return: File generator
        """

        def file_size_M(s):
            digitals = s[:-1]
            if s.endswith('K'):
                return float(digitals) / 1024
            elif s.endswith('M'):
                return float(digitals)
            else:
                return 1024 * float(digitals)

        url = _URL_BASE + _PREF_FILES + self.id
        soup = get_url(url)
        for j in soup.find_all('tr', class_=['tr1', 'tr2']):
            tds = j.find_all('td')
            name = re.search(
                r'getfilelink=([^&]+)&',
                str(j.find(text=lambda text: isinstance(text,
                                                        Comment)))).group(1)
            url = 'http://learn.tsinghua.edu.cn/kejian/data/%s/download/%s' % (
                self.id, name)
            name = re.sub(r'_[^_]+\.', '.', name)
            size = file_size_M(tds[-3].text)
            title = tds[-5].a.text.strip() + name[-4:]
            yield File(size=size, name=name, url=url, title=title)


class Work:
    """
    the homework class
    """

    def __init__(self, url, id, title, start_time, end_time):
        self._url = url
        self._id = id
        self._title = title
        self._details = None
        self._file = None
        self._start_time = start_time
        self._end_time = end_time
        # logging.debug(title)

    @property
    def url(self):
        """work url"""
        return self._url

    @property
    def id(self):
        """work id"""
        return self._id

    @property
    def title(self):
        """work title"""
        return self._title

    @property
    def start_time(self):
        """
        start date of the work
        :return:str time 'yyyy-mm-dd'
        """
        return self._start_time

    @property
    def end_time(self):
        """
        end date of the work
        :return: str time 'yyyy-mm-dd'
        """
        return self._end_time

    @property
    def details(self):
        """
        the description of the work
        :return:str details /None if not exists
        """
        if not self._details:
            soup = get_url(self.url)
            try:
                _details = soup.find_all('td', class_='tr_2')[
                    1].textarea.contents[0]
            except:
                _details = ""
            self._details = _details
        return self._details

    @property
    def file(self):
        """
        the file attached to the work
        :return: Instance of File/None if not exists
        """
        if not self._file:
            soup = get_url(self.url)
            try:
                fname = soup.find_all('td', class_='tr_2')[2].a.contents[0]
                furl = 'http://learn.tsinghua.edu.cn' + \
                    soup.find_all('td', class_='tr_2')[2].a['href']
                _file = File(url=furl, name=fname)
            except(AttributeError):
                _file = None
            self._file = _file
        return self._file


class File:

    def __init__(self, url, name, size=0, note=None, title=None):
        self._name = name
        self._url = url
        self._note = note
        self._size = size
        self._title = title

    def save(self, path='.'):
        filepath = os.path.join(path, self.name)
        if os.path.isfile(filepath):
            return filepath
        if not os.path.exists(path):
            os.makedirs(path)
        r = _session.get(self.url, stream=True)
        with open(filepath, 'wb') as handle:
            if not r.ok:
                raise ValueError('failed in saving file', self.name, self.url)
            for block in r.iter_content(1024):
                handle.write(block)
        return filepath

    @property
    def name(self):
        """file name
        Note! the file name is the name on the web
        but not the name in the download link
        """
        return self._name

    @property
    def title(self):
        """file title
        Note! the file title is the title on the web
        but not the title in the download link
        """
        return self._title

    @property
    def url(self):
        """download url"""
        return self._url

    @property
    def note(self):
        """the description of the file
        this will exits under the CourseFile area but not in work area
        # considering take course.details as note
        """
        return self._note

    @property
    def size(self):
        return self._size


class Message:

    def __init__(self, url, title, date, id):
        self._id = id
        self._url = url
        self._title = title
        self._date = date
        self._details = None
        # logging.debug(title)

    @property
    def id(self):
        return self._id

    @property
    def url(self):
        return self._url

    @property
    def title(self):
        return self._title

    @property
    def date(self):
        return self._date

    @property
    def details(self):
        if not self._details:
            soup = get_url(self.url)
            _details = soup.find_all('td', class_='tr_l2')[
                1].text.replace('\xa0', ' ')
            _details = re.sub('(\\xa0)+', ' ', _details)
            _details = re.sub('\n+', '\n', _details)
            self._details = _details
        return self._details


def test():
    pass


def main():
    test()


if __name__ == '__main__':
    main()
