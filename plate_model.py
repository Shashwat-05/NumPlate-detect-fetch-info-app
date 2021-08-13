import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import cv2 ,easyocr
import matplotlib.pyplot as plt
from numpy import disp


plateCascade = cv2.CascadeClassifier('russian_plate.xml') #can use indian casacde model too

def detect_plate_no(img): #function finds the num plate from pic and returns it
    plateImg = img.copy()
    roi = img.copy()
    plateRect = plateCascade.detectMultiScale(plateImg,scaleFactor = 1.5, minNeighbors = 7)
    for (x,y,w,h) in plateRect:
        roi_ = roi[y:y+h, x:x+w, :]
        platePart = roi[y:y+h, x:x+w, :]
        cv2.rectangle(plateImg,(x+2,y),(x+w-3, y+h-5),(0,255,0),3)
    return plateImg, platePart

def inputImg(imgname): #function takes original pic and sends to above function
    img = cv2.imread(imgname)
    return detect_plate_no(img)

def toText(plate): #converts image characters to text via 'easyocr'
    reader = easyocr.Reader(['en'])
    result = reader.readtext(plate)

    final_result = result[0][1]
    return final_result[:10]
