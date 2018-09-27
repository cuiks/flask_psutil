# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont, ImageFilter

import random


# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))


# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def captcha():
    # 240 x 60:
    width = 40 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('simheittf.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    text = ''
    for t in range(4):
        text_tem = rndChar()
        text = text+text_tem
        draw.text((40 * t + 10, 10), text_tem, font=font, fill=rndColor2())
    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    return image,text

