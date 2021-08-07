import cv2 as cv
import numpy as np

'''
Width = 640
Height = 480
'''
#live camera
cap = cv.VideoCapture(0)
'''
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)
'''
#target image to detect the human body:
imgTarget = cv.imread('TargetImage.jpg')
#myOutfit = cv2.imread('outfit1.jpg')

hT, wT, cT = imgTarget.shape
#myOutfit = cv2.resize(myOutfit,(wT, hT))

orb = cv.ORB(nfeatures=1000)
kp1, des1 = orb.detectAndCompute(imgTarget,None)
#imgTarget = cv.drawKeypoints(imgTarget, kp1, None)

while True:
    sucess, imgWebcam = cap.read()
    
    #display the result:
    cv.imshow('ImageTarget', imgTarget)
    #cv2.imshow('Outfit', myOutfit)
    cv.imshow('Webcamera', imgWebcam)
    cv.waitKey(1)