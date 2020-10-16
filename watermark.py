#!/usr/bin/python

import sys
import cv2 as cv
from skimage.transform import rescale
import os.path


def w_scale(s):
    temp = cv.imread('oil.png')
    temp = cv.cvtColor(temp, cv.COLOR_BGR2GRAY)
    return rescale(temp, s)


def reset():
    return cv.imread('image.jpg')


def save():
    count = 0
    while os.path.isfile('watermarked%d.jpg' % count) is True:
        count += 1
    cv.imwrite('watermarked%d.jpg' % count, image)


def watermarking(x, y, transparent, black):
    for i in range(w_dim[0]):
        for j in range(w_dim[1]):
            if watermark[i, j] != 0:
                for d in range(image.ndim):
                    imx = x + j - int(w_dim[0] / 2)
                    imy = y + i - int(w_dim[0] / 2)
                    if black is True:
                        image[imy, imx, d] = image[imy, imx, d] * (9 - transparent) / 9
                    else:
                        image[imy, imx, d] = image[imy, imx, d] + (255 - image[imy, imx, d]) * (
                                transparent / 9)


def avg_value(x, y):
    temp = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    val_sum = 0
    for i in range(w_dim[0]):
        for j in range(w_dim[1]):
            imx = x + j - int(w_dim[0] / 2)
            imy = y + i - int(w_dim[0] / 2)
            val_sum += temp[imy, imx]
    return val_sum / (w_dim[0] * w_dim[1])


def get_click(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:
        print(x, y)
        ix = x + int(w_dim[1] / 2) + 1
        mix = x - int(w_dim[1] / 2) - 1
        iy = y + int(w_dim[0] / 2) + 1
        miy = y - int(w_dim[0] / 2) - 1
        if (ix >= im_dim[1]) or (iy >= im_dim[0]) or (mix < 0) or (miy < 0):
            print("watermark must be inside image")
        else:
            if avg_value(x, y) > 126:
                black = True
            else:
                black = False
            watermarking(x, y, transparency, black)


image = cv.imread(str(sys.argv[1]))
watermark = cv.imread(str(sys.argv[2]))
watermark = rescale(watermark, 0.2)

w_dim = watermark.shape
im_dim = image.shape
transparency = 5
scale = 0.2

cv.namedWindow('watermarked')
cv.setMouseCallback('watermarked', get_click)
while 1:
    cv.imshow('watermarked', image)
    k = cv.waitKey(20) & 0xFF
    if k == ord('s'):  # save l'image qui a été watermarked
        save()
    elif k == ord('r'):  # reset l'image en chargeant l'originale
        image = reset()
    elif k in [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'),
               ord('9')]:  # niveaux de transparence du watermark
        transparency = k - 48
    elif k == ord('('):  # downscale le watermark
        scale -= 0.05
        if scale <= 0.1:
            scale = 0.05
        watermark = w_scale(scale)
        w_dim = watermark.shape
    elif k == ord(')'):  # upscale le watermark
        scale += 0.05
        watermark = w_scale(scale)
        w_dim = watermark.shape
    elif k == ord('q'):  # quitter
        break
cv.destroyAllWindows()
