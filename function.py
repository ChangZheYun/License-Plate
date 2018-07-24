# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 21:53:58 2018

@author: tizan
"""

import numpy as np
import cv2

def h_v_project(name,x,y,w,h):     #h水平、v垂直
   hsl_pic=cv2.imread(name)
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

def check_rectangle(origin_pic):
 #  check_color=0.0
   index=0.0
   ascent=0
   segment=np.zeros([2,len(gray[0])])
   
   if mode==1:
      standard=150
   else:
      standard=20
      
   for i in range(len(dilation)):
      for j in range(len(dilation[0])):
         if dilation[i][j]==0:
            check_color+=1
         if gray[i][j]<standard:
            segment[0][j]+=1
         index+=1
 #  print("answer ",check_color/index*100)
   if (check_color/index*100)<25:# and (check_color/index*100)>85: #黑色區域佔25%以下淘汰
      return False
   #if (np.sum(segment[0])/index*100)>=15 and (np.sum(segment[0])/index*100)<=75:
   else:
      #往上=>1,往下=>0
      for i in range(0,len(gray[0])-1):
         if segment[0][i]>segment[0][i+1]:
            segment[1][i]=0
         elif segment[0][i]<segment[0][i+1] and (segment[0][i+1]-segment[0][i])>=5:
            segment[1][i]=1
            ascent+=1
      #print(segment)
      if ascent>=8:
         print("answer ",np.sum(segment[0])/index*100)
      #   print(segment)
         return True
      else:
         return False
   #else:
   #   return False
   
cv2.waitKey(0)
cv2.destroyAllWindows()