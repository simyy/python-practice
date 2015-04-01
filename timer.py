#!/usr/bin/env python
#-*- encoding:utf-8 -*-
'''
实现类似于Linux的Crontab的定时程序
'''


import time

from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup

import db
from StudyNotes.scripts.python import page


'''
like crontab in linx, this is a python timer
'''

def tick():
    f = open('blog/test.log', 'w')
    f.write(time.ctime())
    f.close()
    print(time.ctime())

def getmyblog():
    def parse(doc):
        soup = BeautifulSoup(doc)
        blogs = soup.findAll(name='div', attrs={'class':'day'})
        blog_list = []
        for blog in blogs:
            tmp = blog.select('.postTitle')[0].a
            title = tmp.text
            href = tmp['href']
            #print title, href
            summary = blog.select('.postCon')[0].text
            #print summary
            blog_list.append([title, href, summary])
        return blog_list

    site = 'http://www.cnblogs.com/coder2012/'
    myblog = page.page(href=site, parsefunc=parse)
    res = myblog.parse()
    for item in res:
        db.new_post(item[0], item[1], item[2])

class timer:
    '''
    process = timer(function, [para1,para2,...], intervalseconds)
    process.run()
    '''
    def __init__(self, func, paras, seconds, id):
        self.func = func
        self.paras = paras
        self.time = seconds
        self.id = id
        self.scheduler = None
        self.setTimer()

    def setTimer(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.func, 'interval', seconds=self.time, id=self.id)

    def add_job(self, func, seconds, id):
        self.scheduler.add_job(func, 'interval', seconds, id)

    def remove_job(self, id):
        self.scheduler.remove_job(id)


    def run(self):
        self.scheduler.start()

def backgroundrunning(func=tick, args='', time=3, id='default'):
    a = timer(func, args, time, id)
    a.run()

if __name__ == '__main__':
    getmyblog()
