import threading
import cv2 as cv
from xml.dom.minidom import parse

class Minhathread(threading.Thread):
    def __init__(self, img, src, dur):
        self.img = img
        self.src = src
        self.dur = dur
        threading.Thread.__init__(self)

    def run(self):

        imgR = cv.resize(self.img, (600, 600))
        cv.imshow(self.src, imgR)
        cv.waitKey(1000*self.dur)

def mostraImg(imgs, dur):
    threads = []

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

                thread = Minhathread(img, aux.getAttribute('src'), time)
                thread.start()
                threads.append(thread)

    for thread in threads:
        thread.join()


def analiza(tag, durM, flag):


    for info in tag:
        j = 0
        aux = False

        for i in flag:
            if i == info:
                flag.pop(j)
                aux = True
                break
            j += 1
        if aux:
            flag = run(info, durM, flag)
    return flag


def run(tag, durM, flag):

    dur = 100

    flagSeq = tag.getElementsByTagName('seq')
    flagImg = tag.getElementsByTagName('img')
    flagPar = tag.getElementsByTagName('par')


    if tag.getAttribute('dur'):
        dur = tag.getAttribute('dur')
        dur = dur.split('s')
        dur = int(dur[0])

    if flagPar:
        flag = analiza(flagPar, min(durM, dur), flag)
    if flagSeq:
        flag = analiza(flagSeq, min(durM, dur), flag)

    if flagSeq.length == 0 and  flagImg.length > 0 and flagPar.length == 0:
        mostraImg(flagImg, min(dur, durM))
    return flag





doc = parse('slideshow03.xml')
xml = doc.documentElement

estados = xml.getElementsByTagName('par')

flag = estados + xml.getElementsByTagName('seq')
for info in estados:
    durM = 100
    flag = run(info, durM, flag)