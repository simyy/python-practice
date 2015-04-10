import Image
import shutil
import os

"""
 0 - - - - - - - - - - -  - - x                                                                           
 |                            |                                                                           
 |- - x1,y1 - - - - - - - - - |                                                                           
 |      | \\\\\\\\\\\ |       |                                                                           
 |- - - - - - - - - x2,y2 - - |                                                                           
 |                            |                                                                           
 y - - - - - - - - - - - - - -|                                                                           
"""                                                                                                       
                                                                                                          

def cut_img(pic, v_x, v_y, point_a, point_b):
    ''' cut img
        @pic source pic
        @v_x/y virtual x and y
        @port_a/b point(x, y)
    '''
    try:
        img = Image.open(pic)
        (x, y) = img.size

        def trans_xy(x, y, v_x, v_y, point_a, point_b):
            ''' conversion of coordinate
                @x/y length/width of pic
                @v_x/v_y length/width of virtual pic
                @point_a a(x, y)
                @point_b b(x, y)
                @return regoin(x0, y0, x1, y1)
            '''
            a_x = point_a[0]*x/v_x
            a_y = point_a[1]*y/v_y
            b_x = point_b[0]*x/v_x
            b_y = point_b[1]*y/v_y
            return (a_x, a_y, b_x, b_y)

        crop_img = img.crop(trans_xy(x, y, v_x, v_y, point_a, point_b))
        crop_img.save(pic + '.jpg')
        os.remove(pic)
        shutil.move(pic + '.jpg', pic)
    except Exception as e:
        print e
        return False
    return True
