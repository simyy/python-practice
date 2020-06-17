#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""生成简单的包含文字的图片
"""

from PIL import Image, ImageDraw, ImageFont

def circle(ima):
    size = ima.size
    r2 = min(size[0], size[1])
    if size[0] != size[1]:
        ima = ima.resize((r2, r2), Image.ANTIALIAS)
    imb = Image.new('RGBA', (r2, r2),(255,255,255,0))
    pima = ima.load()
    pimb = imb.load()
    r = float(r2/2)
    for i in range(r2):
        for j in range(r2):
            lx = abs(i-r+0.5)
            ly = abs(j-r+0.5)
            l  = pow(lx,2) + pow(ly,2)
            if l <= pow(r, 2):
                pimb[i,j] = pima[i,j]
    return imb

"""
text = raw_input("input a text num: ")
# 新建图片
#img = Image.new("RGB", (100, 60))
img = Image.open('1.png')
# 绘制图片
draw = ImageDraw.Draw(img)
# 字体
font = ImageFont.truetype('simsun.ttc', 40)
# 绘入文字
draw.text((160, 00), ''.join(text), font=font, fill=(255,0,0,255) )
# 保存到文件
img.save('test.png', 'png')
# 显示图片
img.show()
"""
blank = Image.new("RGBA", [60, 60], "red")
im = circle(blank)
#im.show()
font = ImageFont.truetype('simsun.ttc', 40)
draw = ImageDraw.Draw(im)
draw.text((10, 10), '12', font=font, fill=(255,255,255,255) )
#im.show()
im.save("12.png", 'png')

img1 = Image.open('1.png').convert('RGBA')
imm = Image.open('12.png').convert('RGBA')
img1.paste(imm, (0, 0))
img1.show()