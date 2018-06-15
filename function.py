# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 21:53:58 2018

@author: tizan
"""

import numpy as np
import cv2

def h_v_project(name):     #h水平、v垂直
   hsl_pic=cv2.imread('Pre-processing/'+name)
   th = cv2.cvtColor(hsl_pic, cv2.COLOR_BGR2GRAY)
   h_num=np.zeros(300,dtype=int)   #統計水平白點數量
   v_num=np.zeros(500,dtype=int)   #統計垂直白點數量
   horizan=np.array(th)
   vertical=np.array(th)
   
   for i in range(300):
       for j in range(500):
           if not(hsl_pic[i][j]==[0,0,0]).all():
               h_num[i]+=1
               v_num[j]+=1
       for k in range(500): #輸出水平統計圖
           if k<(500-h_num[i]):
               horizan[i][k]=255
           else:
               horizan[i][k]=0
       for m in range(500): #輸出垂直統計圖
           if i<(300-v_num[m]):
               vertical[i][m]=255
           else:
               vertical[i][m]=0

 #  cv2.imshow('horizan',horizan)
 #  cv2.imshow('vertical',vertical)

def check_rectangle(name,x,y,w,h):
   adaptive=cv2.imread('Pre-processing/'+name+'-adpative.jpg') #存成圖片會變成RGB
   #origin_img = cv2.rectangle(origin_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
   count_x=0
   count_y=0
   for i in range(y,y+5):
      for j in range(x,x+w):
         if (adaptive[i][j]==[255,255,255]).any():
            count_x+=1
   for i in range(x,x+5):
      for j in range(y,y+h):
         if (adaptive[j][i]==[255,255,255]).any():
            count_y+=1
   print(count_x,",",count_y)
   if count_x>=500 or count_y>=500:
      return 0
   else:
      return 1
 
cv2.waitKey(0)
cv2.destroyAllWindows()