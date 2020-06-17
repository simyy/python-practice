# -*- coding: UTF-8 -*-
'''
任一个英文的纯文本文件，统计其中的单词出现的个数
'''

import re

def countWordNum(pathname):
    n = 0
    f = open(pathname, 'rb')
    lines = f.readlines()
    for line in lines:
        list = re.findall(r'\b[a-zA-Z]+\b', line, re.MULTILINE)
        n += len(list)
    f.close()
    return n

print countWordNum('word.txt')