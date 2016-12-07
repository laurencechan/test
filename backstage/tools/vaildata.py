# coding=utf-8
import os
import platform

__author__ = 'dolacmeo'
__doc__ = ''

if platform.system() == 'Windows':
    fontType = os.path.dirname(os.path.abspath(__file__)) + '\\CPMono_v07_Black.otf'
else:
    fontType = os.path.dirname(os.path.abspath(__file__)) + '/CPMono_v07_Black.otf'


def generate_authenticode():
    from PIL import Image, ImageDraw, ImageFont
    import random
    letters = random.sample('abcdefghjkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ23456789', 4)
    width = 100
    height = 40
    im = Image.new("RGB", (width, height), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(fontType, 30)
    for i in range(4):
        dr.text((5 + i * 20, 5), letters[i],
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), font)
    del dr

    for x in range(width):
        for y in range(height):
            if im.getpixel((x, y)) == (255, 255, 255):
                im.putpixel((x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    import base64
    from io import BytesIO
    out = BytesIO()
    im.save(out, "PNG")
    imgstr = base64.b64encode(out.getvalue()).decode('ascii')
    img_tag = '<img src="data:image/png;base64,{0}">'.format(imgstr)
    return ''.join(letters), img_tag

if __name__ == "__main__":
    # print generate_authenticode()
    pass
