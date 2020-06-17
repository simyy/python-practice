#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""生成简单的包含文字的图片
"""

from PIL import Image, ImageDraw, ImageFont

# 新建图片
#img = Image.new("RGB", (100, 60))
img = Image.open('2.png')
# 绘制图片
draw = ImageDraw.Draw(img)
# 字体
font = ImageFont.truetype('simsun.ttc', 20)
# 绘入文字
draw.text((10, 20), u"test 测试", font=font)
# 保存到文件
img.save('test.png', 'png')
# 显示图片
img.show()