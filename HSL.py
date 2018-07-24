# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 20:19:33 2018

@author: tizan
"""

import cv2
import numpy as np

def L_threshold(origin_pic): #找出圖片HSL的L門檻值
   pic = cv2.cvtColor(origin_pic, cv2.COLOR_BGR2HLS)
   
# =============================================================================
#    #更換儲存名稱(rfind從後面找起)
#    name=name.replace(name[name.rfind('/')+1:name.find('.jpg')],"HSL",1)
#    cv2.imwrite(name,pic)
# =============================================================================
   
   L_num=np.zeros([257],dtype=int) #統計L數量
   average=0.0
   variance=0.0
   index=0                         #找出最適合的L門檻

   for i in range(300):
       for j in range(500):
           L_num[pic[i][j][1]]+=1
           average+=pic[i][j][1]
   average/=150000
   
   for i in range(256):
      variance+=((i-average)**2)*L_num[i]
   variance/=150000
   
   for i in range(255,0,-1):
       L_num[256]+=L_num[i]
       if L_num[256]>=30000:
           index=i
           break
       
   print('L門檻:',index,'\n')
   print('average=',average)
   print('variance=',variance)
  # print(L_num)
   if variance>3500:       
      return origin_pic
   
   for i in range(300):
       for j in range(500):
           if pic[i][j][1]<index:# or pic[i][j][2]>120:
               pic[i][j]=[0,0,0]
   cv2.imshow('HSL',pic)   

   return pic

cv2.waitKey(0)
cv2.destroyAllWindows()
