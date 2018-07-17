# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 02:36:58 2018

@author: tizan
"""

name='car9'

capture=cv2.VideoCapture('Data/'+name+'.mp4')
count=1
time=10         
#建立前處理資料夾(放前處理照片)
if not os.path.isdir('Pre-processing'): 
   os.mkdir('Pre-processing')

#建立圖片資料夾
picture_path='Pre-processing/'+name+'/'
if not os.path.isdir(picture_path):
   os.mkdir(picture_path)
   
if capture.isOpened():
   while True:
      ret,prev=capture.read()
      if ret==True and count%time==0:
         prev = cv2.resize(prev,(500,300))
         cv2.imwrite(picture_path+'resize.jpg',prev)
         
         #HSL處理
         index=HSL.L_threshold(picture_path+'resize.jpg')
         HSL.SL_filter(picture_path+'HSL.jpg',index)
         # =============================================================================
         # print('L門檻=',index,'\n')
         # hsl_pic = cv2.imread(picture_path+'L_filter.jpg')
         # cv2.imshow('HLS-Lfilter',hsl_pic)
         # =============================================================================
         
         origin_pic1 = cv2.imread(picture_path+'SL_filter.jpg')
         pic = cv2.cvtColor(origin_pic1, cv2.COLOR_BGR2GRAY)
         cv2.imshow('hsl',origin_pic1)
         #雙邊濾波 50=鄰域直徑大小
         pic=cv2.bilateralFilter(pic,50,30,30) 
         #cv2.imshow('bilaterlFilter',pic)
         
         #適應性二值化
         pic = cv2.adaptiveThreshold(pic, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 57, 6)
         cv2.imwrite(picture_path+'adaptive.jpg',pic)
         
         #開運算
         kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
         pic = cv2.morphologyEx(pic, cv2.MORPH_OPEN, kernel)
         #cv2.imshow('erode',pic)
         
         pic = cv2.medianBlur(pic, 5)
         
         #pip install opencv-contrib-python
         #gray=cv2.cvtColor(origin_pic, cv2.COLOR_BGR2GRAY)
         sift = cv2.xfeatures2d.SIFT_create()
         kps, features = sift.detectAndCompute(pic, None)
         cv2.drawKeypoints(prev,kps,prev,(0,255,255),flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
         cv2.imshow('sift',prev)
         
         _1, contours, _2 = cv2.findContours(pic, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
         for i in range(len(contours)):
             cnt = contours[i]
             x, y, w, h = cv2.boundingRect(cnt)
             if w>h and w+h>100 and w+h<600:
                prev = cv2.rectangle(prev, (x, y), (x+w, y+h), (255, 0, 0), 2)

         cv2.imshow('capture',prev)
      elif ret==False:
         break
      count+=1
      if cv2.waitKey(20)==27:  
            break  
