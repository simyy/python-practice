# -*- coding: UTF-8 -*-
'''
做为 Apple Store App 独立开发者，你要搞限时促销，
为你的应用生成激活码（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）？
'''
import hashlib
import time
import datetime

def getmd5(key):
    myMd5 = hashlib.md5()
    myMd5.update(key)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest


def getTimems():
    t = str(datetime.datetime.now())
    return t.replace(':', '').replace('-','')\
        .replace(' ', '').replace('.', '')


def createActiveCode(n):
    set = {}
    lists = []
    i = 0
    while i < n:
        tmp = getmd5(getTimems())[0:20]
        if not set.has_key(tmp):
            set[tmp] = 0
            tmp = tmp[:5] + '-' + tmp[5:10] + '-'\
                    + tmp[10:15] + '-' + tmp[15:]
            lists.append(tmp)
            i += 1
    return lists

print createActiveCode(5)