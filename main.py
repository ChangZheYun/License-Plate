# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 19:58:17 2018

@author: tizan
"""

import cv2
import os
import time
import HSL
import function

tStart = time.time() #計時開始

name='car7'
origin_pic = cv2.imread('Data/'+name+'.jpg')
origin_pic = cv2.resize(origin_pic,(500,300))
mode=0  #1:圖片過亮(不適合用HSL)，2:適合用HSL
# =============================================================================
# 
# #建立前處理資料夾(放前處理照片)
# if not os.path.isdir('Pre-processing'): 
#    os.mkdir('Pre-processing')
# 
# #建立圖片資料夾
# picture_path='Pre-processing/'+name+'/'
# if not os.path.isdir(picture_path):
#    os.mkdir(picture_path)
#    
# cv2.imwrite(picture_path+'resize.jpg',origin_pic)
# =============================================================================

#HSL判斷
HSL_pic=HSL.L_threshold(origin_pic)

if (HSL_pic==origin_pic).all():
   gray = cv2.cvtColor(origin_pic, cv2.COLOR_BGR2GRAY)
   mode=1
else:
   gray = cv2.cvtColor(HSL_pic, cv2.COLOR_BGR2GRAY)
   mode=2


# =============================================================================
# gray=cv2.cvtColor(origin_pic, cv2.COLOR_BGR2GRAY)
# test=cv2.cornerHarris(gray,2,3,0.01)
# test = cv2.dilate(test,None)
# origin_pic[test>0.01*test.max()]=[0,0,255]
# cv2.imshow('ori',origin_pic)
# =============================================================================

#gray = cv2.equalizeHist(gray)
cv2.imshow('gray',gray)

#雙邊濾波 50=鄰域直徑大小
pic=cv2.bilateralFilter(gray,50,30,30) 
#cv2.imshow('bilaterlFilter',pic)

#適應性二值化
adath = cv2.adaptiveThreshold(pic, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 5)
#cv2.imwrite(picture_path+'adaptive.jpg',adath)
cv2.imshow('threshold',adath)

#if mode==1:
median = cv2.medianBlur(adath, 5)
cv2.imshow('median',median)
  # adath=cv2.Sobel(adath,cv2.CV_16S,1,1)
  # adath = cv2.convertScaleAbs(adath)
  # cv2.imshow('sobel',adath)
  # adath = cv2.Laplacian(adath,cv2.CV_16S,ksize = 3)
  # adath = cv2.convertScaleAbs(adath)
  # cv2.imshow('laplacian',adath)
   
#開運算
#kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
#pic = cv2.morphologyEx(adath, cv2.MORPH_OPEN, kernel)
#cv2.imshow('erode',pic)

#mode1雜訊較多
if mode==1:
   erosion = cv2.erode(median, None , iterations= 3 ) 
   dilation = cv2.dilate(erosion, None , iterations= 3 )
elif mode==2:
   erosion = cv2.erode(median, None , iterations= 2 ) 
   dilation = cv2.dilate(erosion, None , iterations= 2 )

cv2.imshow('dilation',dilation)

# =============================================================================
# #中值濾波去胡椒鹽雜訊
# pic = cv2.medianBlur(dilation, 5)
# cv2.imshow('median',pic)
# 
# =============================================================================
# =============================================================================
# #pip install opencv-contrib-python
# #gray=cv2.cvtColor(origin_pic, cv2.COLOR_BGR2GRAY)
# sift = cv2.xfeatures2d.SIFT_create()
# kps, features = sift.detectAndCompute(pic, None)
# cv2.drawKeypoints(origin_pic,kps,origin_pic,(0,255,255),flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# cv2.imshow('sift',origin_pic)
# =============================================================================


_1, contours, _2 = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#_1, contours2, _2 = cv2.findContours(median, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(contours)):
    cnt = contours[i]
    x, y, w, h = cv2.boundingRect(cnt)
    check=function.check_rectangle(mode,gray[y:y+h,x:x+w],dilation[y:y+h,x:x+w],x,y,w,h)
    if w>h and check==True:
       origin_pic = cv2.rectangle(origin_pic, (x, y), (x+w, y+h), (255, 255, 0), 2)
# =============================================================================
# 
# for i in range(len(contours2)):
#     cnt = contours2[i]
#     x, y, w, h = cv2.boundingRect(cnt)
#     check=function.check_rectangle(mode,gray[y:y+h,x:x+w],dilation[y:y+h,x:x+w],x,y,w,h)
#     if w>h and check==True:
#        origin_pic = cv2.rectangle(origin_pic, (x, y), (x+w, y+h), (255, 255, 0), 2)
# 
# =============================================================================
    

cv2.imshow('rectangle', origin_pic)

tEnd = time.time()#計時結束
print(tEnd - tStart)

cv2.waitKey(0)
cv2.destroyAllWindows()
