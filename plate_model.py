import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import cv2 ,easyocr
import matplotlib.pyplot as plt
from numpy import disp


plateCascade = cv2.CascadeClassifier('russian_plate.xml')

def detect_plate_no(img):
    plateImg = img.copy()
    roi = img.copy()
    plateRect = plateCascade.detectMultiScale(plateImg,scaleFactor = 1.5, minNeighbors = 7)
    for (x,y,w,h) in plateRect:
        roi_ = roi[y:y+h, x:x+w, :]
        platePart = roi[y:y+h, x:x+w, :]
        cv2.rectangle(plateImg,(x+2,y),(x+w-3, y+h-5),(0,255,0),3)
    return plateImg, platePart

#img = cv2.imread('D:\\SUMMER PROGRAM\\tasks\\task8\\a.jpg')

def display_plate_no(img):
    img_ = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.imshow(img_)
    plt.show()

def inputImg(imgname):
    img = cv2.imread(imgname)
    return detect_plate_no(img)

#inpImg, plate = detect_plate_no(inputImg)
#display_plate_no(inpImg)
#display_plate_no(plate)

def toText(plate):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(plate)

    final_result = result[0][1]
    n=""
    f = final_result.split('-')
    f = n.join(f)
    f = f.replace(" ","")
    plate_number = f.upper()
    return plate_number[:10]
