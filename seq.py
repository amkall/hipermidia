import cv2 as cv
import numpy
from xml.dom.minidom import parse

def mostraImag(imgs, dur):

    for aux in imgs:
        img = cv.imread(aux.getAttribute('src'), 1)
        time = aux.getAttribute('dur')
        time = time.split('s')
        time = int(time[0])


        if time > dur:
            time = dur
            dur = 0
        else:
            dur -= time


        if time > 0:
            imgR = cv.resize(img, (600, 600))
            cv.imshow(aux.getAttribute('src'), imgR)

            cv.waitKey(time * 1000)
            cv.destroyWindow(aux.getAttribute('src'))


def run(seq, durM, flag):
    dur = 100

    flagSeq = seq.getElementsByTagName('seq')
    flagImg = seq.getElementsByTagName('img')

    if seq.getAttribute('dur'):
        dur = seq.getAttribute('dur')
        dur = dur.split('s')
        dur = int(dur[0])


    if flagSeq:

        for info in flagSeq:
            j = 0
            aux = False

            for i in flag:
                if i == info:
                    flag.pop(j)
                    aux = True
                    break
                j += 1
            if aux:
                flag = run(info, min(dur, durM), flag)


    if flagSeq.length == 0 and flagImg.length > 0:
      mostraImag(flagImg, min(dur, durM))

    return flag




doc = parse('slideshow02.xml')
xml = doc.documentElement

estado = xml.getElementsByTagName('seq')

flag = estado
for seq in estado:
    flag = run(seq, 100, flag)

