# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 19:58:17 2018

@author: tizan
"""

import cv2
import os
import HSL
import function

name='car3'
origin_pic = cv2.imread(name+'.jpg')
origin_pic = cv2.resize(origin_pic,(500,300))
os.system("md Pre-processing")    #建立前處理資料夾(放前處理照片)
cv2.imwrite('Pre-processing/'+name+'-resize.jpg',origin_pic)

#HSL處理
index=HSL.L_threshold(name+'-resize')
HSL.SL_filter(name,index)
# =============================================================================
# print('L門檻=',index,'\n')
# hsl_pic = cv2.imread('Pre-processing/'+name+'-L_filter.jpg')
# cv2.imshow('HLS-Lfilter',hsl_pic)
# =============================================================================
origin_pic1 = cv2.imread('Pre-processing/'+name+'-SL_filter.jpg')
pic = cv2.cvtColor(origin_pic1, cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray',pic)

#雙邊濾波 50=鄰域直徑大小
pic=cv2.bilateralFilter(pic,50,30,30) 
#cv2.imshow('bilaterlFilter',pic)

#適應性二值化
pic = cv2.adaptiveThreshold(pic, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 57, 6)
cv2.imwrite('Pre-processing/'+name+'-adpative.jpg',pic)
cv2.imshow('threshold',pic)
#開運算
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
pic = cv2.morphologyEx(pic, cv2.MORPH_OPEN, kernel)
#cv2.imshow('erode',pic)

pic = cv2.medianBlur(pic, 5)

_1, contours, _2 = cv2.findContours(pic, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for i in range(len(contours)):
    cnt = contours[i]
    x, y, w, h = cv2.boundingRect(cnt)
    if w>h and w+h>100 and w+h<400:
       check=function.check_rectangle(name,x,y,w,h)
       if check==1:
        origin_pic = cv2.rectangle(origin_pic, (x, y), (x+w, y+h), (255, 0, 0), 2)
    

cv2.imshow('rectangle', origin_pic)

cv2.waitKey(0)
cv2.destroyAllWindows()
