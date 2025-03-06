import cv2
import numpy as np
import os
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices=false'

import tensorflow as tf
from tensorflow import keras

model_path = "/home/aman/Projects/traffic-recognition/ml/src/models"
model = keras.models.load_model(model_path + "/TSModel.keras")

def get_redness(img):
    yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
    y,u,v = cv2.split(yuv)
    return v

def set_threshold(img, t=150):
    # Apply threshold to the single-channel image
    ret, thresholded = cv2.threshold(img, t, 255, cv2.THRESH_BINARY)
    return thresholded


def findContour(img):
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def findBiggestContour(contours):
    m = 0
    c = [cv2.contourArea(i) for i in contours]
    return contours[c.index(max(c))]

def bounding_box(img, contours):
    x, y, w, h = cv2.boundingRect(contours)
    img = cv2.rectangle(img,(x,y), (x+w,y+h), (0,255,0), 2)
    sign = img[y:(y+h), x:(x+w)]
    return img, sign

def preprocessingImageToClassifier(image=None,imageSize=28,mu=89.77428691773054,std=70.85156431910688):
    image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    image = cv2.resize(image,(imageSize,imageSize))
    image = (image - mu) / std
    image = image.reshape(1,imageSize,imageSize,1)
    return image

def predict(sign):
	img = preprocessingImageToClassifier(sign,imageSize=28)
	return np.argmax(model.predict(img))

labelToText = { 0:"Stop",
    			1:"Do not Enter",
    			2:"Traffic jam is close",
    			3:"Yeild"}


cap = cv2.VideoCapture(0)

while(True):
    _, frame = cap.read()
    redness = get_redness(frame)
    treshold = set_threshold(redness)
    try:
        contours = findContour(treshold)
        big_contour = findBiggestContour(contours)
        if cv2.contourArea(big_contour) > 3000:
            print(cv2.contourArea(big_contour))
            img, sign = bounding_box(frame, big_contour)
            cv2.imshow('Frame: ',frame)
            cv2.imshow('Sign: ', sign)
            print("Now,I see:",labelToText[predict(sign)])
        else:
            cv2.imshow('Frame: ', frame)
            
    except:
        cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()