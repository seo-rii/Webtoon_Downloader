import os

import numpy as np
from PIL import Image
from img2pdf import convert

from module.log import log
from module.webtooninfo import getWebtoonName


def mergeImage(op, webtoonId, viewNo, cutNo, savePath, tmpPath, runningThreadNo, cookie):
    file_list = []
    size_y = []
    ti = Image.open(
        os.path.join(tmpPath, getWebtoonName(op, webtoonId, cookie) + "_" + str(viewNo) + "_" + str(0) + ".png"))
    nx = ti.size[0]
    ti.close()
    for i in range(0, cutNo):
        file = os.path.join(tmpPath, getWebtoonName(op, webtoonId, cookie) + "_" + str(viewNo) + "_" + str(i) + ".png")
        image = Image.open(file)
        im = image.resize((nx, int(image.size[1] / image.size[0] * nx)))
        file_list.append(im)
        size_y.append(im.size[1])
        image.close()
    ny = sum(size_y)
    canv = Image.new("RGB", (nx, ny), (256, 256, 256))
    sumY = 0
    for idx in range(len(file_list)):
        area = (0, sumY, nx, size_y[idx] + sumY)
        canv.paste(file_list[idx], area)
        sumY = sumY + size_y[idx]
    canv.save(os.path.join(savePath, getWebtoonName(op, webtoonId, cookie) + "_" + str(viewNo) + '.png'), 'PNG')
    log("m " + str(viewNo), 3)
    runningThreadNo.value -= 1


def alpha_composite(front, back):
    """Alpha composite two RGBA images.
    Source: http://stackoverflow.com/a/9166671/284318
    Keyword Arguments:
    front -- PIL RGBA Image object
    back -- PIL RGBA Image object
    """
    front = np.asarray(front)
    back = np.asarray(back)
    result = np.empty(front.shape, dtype='float')
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    falpha = front[alpha] / 255.0
    balpha = back[alpha] / 255.0
    result[alpha] = falpha + balpha * (1 - falpha)
    old_setting = np.seterr(invalid='ignore')
    result[rgb] = (front[rgb] * falpha + back[rgb] * balpha * (1 - falpha)) / result[alpha]
    np.seterr(**old_setting)
    result[alpha] *= 255
    np.clip(result, 0, 255)
    result = result.astype('uint8')
    result = Image.fromarray(result, 'RGBA')
    return result


def mergeImagePdf(op, webtoonId, viewNo, cutNo, savePath, tmpPath, runningThreadNo, cookie, noProgressBar):
    pdf_list = []
    for i in range(0, cutNo):
        im = Image.open(
            os.path.join(tmpPath, getWebtoonName(op, webtoonId, cookie) + "_" + str(viewNo) + "_" + str(i) + ".png"))
        if len(im.getbands()) == 4:
            back = Image.new('RGBA', size=im.size, color=(255, 255, 255) + (255,))
            im = alpha_composite(im, back).convert('RGB')
            im.save(os.path.join(tmpPath,
                                 getWebtoonName(op, webtoonId, cookie) + "_" + str(viewNo) + "_" + str(i) + ".png"))
        pdf_list.append(
            os.path.join(tmpPath, getWebtoonName(op, webtoonId, cookie) + "_" + str(viewNo) + "_" + str(i) + ".png"))
    pdf = convert(pdf_list)
    with open(os.path.join(savePath, getWebtoonName(op, webtoonId, cookie) + "_" + str(viewNo) + '.pdf'), "wb") as f:
        f.write(pdf)
    if noProgressBar:
        log("m " + str(viewNo), 3)
    runningThreadNo.value -= 1
