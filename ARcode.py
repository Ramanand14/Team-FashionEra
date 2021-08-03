import cv2
import numpy as np
'''
Width = 640
Height = 480
'''
#live camera
cap = cv2.VideoCapture(0)
'''
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)
'''
#target image to detect the human body:
imgTarget = cv2.imread('TargetImage.jpg')

while True:
    sucess, imgWebcam = cap.read()
    
    #display the result:
    cv2.imshow('ImageTarget', imgTarget)
    cv2.imshow('Webcamera', imgWebcam)
    cv2.waitKey(1)