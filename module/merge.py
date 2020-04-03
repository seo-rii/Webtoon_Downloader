import os

from PIL import Image
from img2pdf import convert

from module.log import log
from module.webtooninfo import getWebtoonName


def mergeImage(op, webtoonId, viewNo, cutNo, savePath, runningThreadNo, cookie):
    file_list = []
    size_y = []
    ti = Image.open(
        os.path.join(savePath, "tmp",
                     getWebtoonName(op, webtoonId, cookie) + "_" + str(viewNo) + "_" + str(0) + ".png"))
    nx = ti.size[0]
    ti.close()
    for i in range(0, cutNo):
        file = os.path.join(savePath, "tmp",
                            getWebtoonName(op, webtoonId, cookie) + "_" + str(viewNo) + "_" + str(i) + ".png")
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


def mergeImagePdf(op, webtoonId, viewNo, cutNo, savePath, runningThreadNo, cookie):
    pdf_list = []
    for i in range(0, cutNo):
        pdf_list.append(
            os.path.join(savePath, "tmp",
                         getWebtoonName(op, webtoonId, cookie) + "_" + str(viewNo) + "_" + str(i) + ".png"))
    pdf = convert(pdf_list)
    with open(os.path.join(savePath, getWebtoonName(op, webtoonId, cookie) + "_" + str(viewNo) + '.pdf'), "wb") as f:
        f.write(pdf)
    log("m " + str(viewNo), 3)
    runningThreadNo.value -= 1
