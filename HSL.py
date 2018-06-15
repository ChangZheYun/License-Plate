# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 20:19:33 2018

@author: tizan
"""

import cv2
import numpy as np
import function

def L_threshold(name): #找出圖片HSL的L門檻值
   origin_pic = cv2.imread('Pre-processing/'+name+'.jpg')
   pic = cv2.cvtColor(origin_pic, cv2.COLOR_BGR2HLS)
   name=name.replace(name[name.find('-',0,len(name)):len(name)],"-HSL",1) #將name的名字更改
   cv2.imwrite('Pre-processing/'+name+'.jpg',pic)
   
   L_num=np.zeros([257],dtype=int) #統計L數量
   index=0                         #找出最適合的L門檻

   for i in range(300):
       for j in range(500):
           L_num[pic[i][j][1]]+=1
           
   for i in range(255,0,-1):
       L_num[256]+=L_num[i]
       if L_num[256]>=10000:
           index=i
           break
       
   print('L門檻:',index,'\n')
   return index
   
def SL_filter(name,index):
   hls_pic = cv2.imread('Pre-processing/'+name+'-HSL.jpg')
   for i in range(300):
       for j in range(500):
           if hls_pic[i][j][1]<index or hls_pic[i][j][2]>175:
               hls_pic[i][j]=[0,0,0]
   cv2.imwrite('Pre-processing/'+name+'-SL_filter.jpg',hls_pic)
   cv2.imshow('SL_filter',hls_pic)
   function.h_v_project(name+'-SL_filter.jpg')

cv2.waitKey(0)
cv2.destroyAllWindows()
