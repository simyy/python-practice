#!/usr/bin/env
# encoding:utf-8

'''
利用PIL库实现的改变图像的尺寸，实际使用中可用来生成缩略图
'''

import Image
import types

#@size   为修改后的尺寸，可以为一个元组（x,y），也可以为一个x(等比例缩放)
#@input  图片路径
#@output 保存文件路径，必须有后缀名,xxx.jpg或xxx.png
def smallPic(size, input, output):
    img = Image.open(input)
    if type(size) is types.TupleType:
        x_s, y_s = size
    else:
      (x, y) = img.size
      x_s = size
      y_s = y * x_s / x
    out = img.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(output)
