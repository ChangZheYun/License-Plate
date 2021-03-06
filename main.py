# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 19:58:17 2018
@author: tizan

"""

import cv2
import time
import HSL
import numpy as np
import os
import function

tStart = time.time() #計時開始
for image in range(1,46):
   origin_pic = cv2.imread('Data/car'+str(image)+'.jpg')
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
   #cv2.imshow('gray',gray)
   
   #雙邊濾波 50=鄰域直徑大小
   pic=cv2.bilateralFilter(gray,50,30,30) 
   #cv2.imshow('bilaterlFilter',pic)
   
   #適應性二值化
   adath = cv2.adaptiveThreshold(pic, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 5)
   #cv2.imwrite(picture_path+'adaptive.jpg',adath)
   #cv2.imshow('threshold',adath)
   
   #if mode==1:
   median = cv2.medianBlur(adath, 5)
   #cv2.imshow('median',median)
     # adath=cv2.Sobel(adath,cv2.CV_16S,1,1)
     # adath = cv2.convertScaleAbs(adath)
     # cv2.imshow('sobel',adath)
     # adath = cv2.Laplacian(adath,cv2.CV_16S,ksize = 3)
     # adath = cv2.convertScaleAbs(adath)
      
   #開運算
     # cv2.imshow('laplacian',adath)
   #kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
   #pic = cv2.morphologyEx(adath, cv2.MORPH_OPEN, kernel)
   #cv2.imshow('erode',pic)
   
   erosion = cv2.erode(median, None , iterations= 3 ) 
   dilation = cv2.dilate(erosion, None , iterations= 3 )
   #cv2.imshow('dilation',dilation)
   
   # =============================================================================
   # #pip install opencv-contrib-python
   # #gray=cv2.cvtColor(origin_pic, cv2.COLOR_BGR2GRAY)
   # sift = cv2.xfeatures2d.SIFT_create()
   # kps, features = sift.detectAndCompute(pic, None)
   # cv2.drawKeypoints(origin_pic,kps,origin_pic,(0,255,255),flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
   # cv2.imshow('sift',origin_pic)
   # =============================================================================
   
   _1, contours, _2 = cv2.findContours(dilation,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   _1, contours2, _2 = cv2.findContours(median, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   contours+=contours2
   
# =============================================================================
#    M=cv2.getRotationMatrix2D((column/2,row/2),-10,1)
#    origin_pic = cv2.warpAffine(origin_pic,M,(column,row))
#    cv2.imshow('b',origin_pic)
# =============================================================================
   
   counter=1
   for i in range(len(contours)):
       cnt = contours[i]
       #rec=>第一個是旋轉後距形的左上角X,Y值，第二個是寬及高，第三個是旋轉的角度theta（或視為傾斜角度）
       rect=cv2.minAreaRect(cnt)
       box = cv2.boxPoints(rect)
       box = np.int0(box) #省略小數點後方數字
       if rect[1][0]>20 and rect[1][1]>10 and (1.3<=(rect[1][0]/rect[1][1])<=4 or 1.3<=(rect[1][1]/rect[1][0])<=4):
          #cv2.drawContours(origin_pic,[box],0,(0,0,255),2)
          #origin_pic = cv2.rectangle(origin_pic, (x, y), (x+w, y+h), (255, 0, 0), 2)
          #cv2.imwrite('HAHA/test'+str(i)+'.jpg',origin_pic[y:y+h,x:x+w])
          #利用boundingRect找出最小長方形(無旋轉)
          #x, y, w, h = cv2.boundingRect(cnt)
          #rectangle=origin_pic[y:y+h,x:x+w]
          #rotate=cv2.getRotationMatrix2D(((x+w)/2,(y+h)/2),rect[2],1)
          #rectangle = cv2.warpAffine(rectangle,rotate,(x+w,y+h))
          p1=np.float32([[box[0][0],box[0][1]],[box[1][0],box[1][1]],[box[2][0],box[2][1]],[box[3][0],box[3][1]]])
          if box[0][0]>box[2][0]:
             p2=np.float32([[256,128],[0,128],[0,0],[256,0]])
          else:
             p2=np.float32([[0,128],[0,0],[256,0],[256,128]])
            
          perspective=cv2.getPerspectiveTransform(p1,p2)
          rectangle=cv2.warpPerspective(origin_pic,perspective,(256,128))
          
          picture_path='possible area/car'+str(image)+'/'
          if not os.path.isdir(picture_path):
             os.mkdir(picture_path)
          cv2.imwrite(picture_path+str(counter)+'.jpg',rectangle)
          
          counter+=1
         # check=function.check_rectangle(rectangle)
          
          
   # =============================================================================
   #     x, y, w, h = cv2.boundingRect(cnt)
   #    # check=function.check_rectangle(mode,gray[y:y+h,x:x+w],dilation[y:y+h,x:x+w],x,y,w,h)
   #    # if w>h and check==True:
   #     origin_pic = cv2.rectangle(origin_pic, (x, y), (x+w, y+h), (255, 255, 0), 2)
   # 
   # =============================================================================
   
   #cv2.imshow('rectangle', origin_pic)
   
   tEnd = time.time()#計時結束
   print(tEnd - tStart)

   cv2.waitKey(0)
   cv2.destroyAllWindows()
