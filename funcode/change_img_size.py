# -*- encoding:utf-8 -*-
'''
你有一个目录，装了很多照片，把它们的尺寸变成都不大于 iPhone5 分辨率的大小。
'''

import os
import threading
from PIL import Image

Const_Image_Format = [".jpg", ".jpeg", ".bmp", ".png"]

#单进程实现
def changeImgSize1(pathname, size):
    global Const_Image_Format
    dirs = os.listdir(pathname)
    for dir in dirs:
        st = dir.rfind('.')
        if st != -1 and dir[st:] in Const_Image_Format:
            print dir
            img = Image.open(pathname + '/' + dir)
            x, y = img.size
            out = img.resize(size, Image.ANTIALIAS)
            out.save('picture/change/' + dir)


def changeImg(pathname, img, size, outpath):
    im = Image.open(pathname + '/' + img)
    out = im.resize(size, Image.ANTIALIAS)
    out.save(outpath + '/' + img)

class changeImgThread(threading.Thread):
    def __init__(self, pathname, imgs, size, outpath):
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.imgs = imgs
        self.size = size
        self.pathname = pathname
        if outpath[-1] == '/':
            self.outpath = outpath[0:-1]
        else:
            self.outpath = outpath

    def run(self):
        for img in self.imgs:
            changeImg(self.pathname, img, self.size, self.outpath)

    def stop(self):
        pass

#多线程实现
def changeImgSize2(pathname, size, num, outpath):
    global Const_Image_Format
    dirs = os.listdir(pathname)
    dirstmp = []
    for dir in dirs:
        st = dir.rfind('.')
        if st != -1 and dir[st:] in Const_Image_Format:
            dirstmp.append(dir)
    n = len(dirstmp)
    t = n/num
    j = 0
    i = 0
    changthread = []
    while i < num:
        print i,j,n,num
        if j > n:
            return
        imgs = []
        if n - j >= t:
            imgs = dirstmp[j:j+t]
        else:
            imgs = dirstmp[j:]
        print imgs
        changethread = changeImgThread(pathname, imgs, size, outpath)
        changethread.start()
        j += t
        i += 1
        print i,j,n,num


size = [200, 200]
#changeImgSize1('picture', size)
changeImgSize2('picture', size, 3, 'picture/change')