from PIL import Image, ImageFont, ImageDraw
from random import randrange, sample, choice
import StringIO

'''
1. wget http://effbot.org/downloads/Imaging-1.1.7.tar.gz
   yum install freetype-devel
2. 修改setup.py文件 FREETYPE_ROOT = '/usr/lib64','/usr/include/freetype2/freetype'
   python setup.py build_ext -i
   python setup.py install
'''

def get_verify_code(request):
    """
    background #随机靠山色彩
    line_color #随机干扰线色彩
    img_width = #画布宽度
    img_height = #画布高度
    font_color = #验证码字体色彩
    font_size = #验证码字体尺寸
    font = I#验证码字体
    """

    img_width = 58
    img_height = 30
    font_size = 16
    font_color = ['black','darkblue','darkred']
    codes = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    background = (randrange(230,255),randrange(230,255),randrange(230,255))
    line_color = (randrange(0,255),randrange(0,255),randrange(0,255))

    font = ImageFont.truetype("%s"%CODE_FILE,font_size)

    #新建画布
    im = Image.new('RGB',(img_width,img_height),background)
    draw = ImageDraw.Draw(im)
    code = ''.join(sample(codes,4))
    #新建画笔
    draw = ImageDraw.Draw(im)

    #画干扰线
    for i in range(randrange(3,5)):
        xy = (randrange(0,img_width),randrange(0,img_height),
              randrange(0,img_width),randrange(0,img_height))
        draw.line(xy,fill=line_color,width=1)

    #写入验证码文字
    x = 2
    for i in code:
        y = randrange(0,10)
        draw.text((x,y), i, font=font, fill=choice(font_color))
        x += 14
    buf = StringIO.StringIO()
    im.save(buf,'gif')
    buf.seek(0)
    request.session['authcode'] = code.lower()
    return HttpResponse(buf.getvalue(),'image/gif')
