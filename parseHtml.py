#!/usr/bin/env python
#-*- encoding:utf-8 -*-

'''
if you want to crawl pages, then use urllib2 to download it and bs4 to parse it.
如果希望爬取网页内容，可以使用urllib2下载页面内容，用bs4来解析网页内容。
'''

import urllib2

from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

'''
parse page class
'''

site = 'http://www.cnblogs.com/'

class page():
    '''
    import page
    result = page.page(href='www.baidu.com', parsefunc=parse())
    '''
    def __init__(self, href=site, parsefunc=None):
        self.href = href
        self.doc = ''
        self.parsefunc = parsefunc
        self.loadPage()

    def loadPage(self):
        try:
            self.doc = urllib2.urlopen(self.href).read()
        except Exception as e:
            print 'urlopen error: ',e
            return ''

    def parse(self):
        self.loadPage()
        return self.parsefunc(self.doc)

    def find(self, name='', attrs={}):
        soup = BeautifulSoup(self.doc, from_encoding='gbk')
        result = soup.findAll(name=name, attrs=attrs)


if __name__ == '__main__':
    a = page()
    print a.parse()
