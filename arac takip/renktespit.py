#!/usr/bin/env python3
import numpy as np
import cv2
import pickle
import time
import math
        
        
width=640
height=480
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

#cv2.namedWindow('myTracker')
#cv2.moveWindow('myTracker',width,0)

hueLow=0
hueHigh=255
satLow=205
satHigh=255
valLow=80
valHigh=255

sayac=0
while True:
    orta_x=int(width/2)
    orta_y=int(height/2)
    
    ignore,  frame = cam.read(0)
    
    frameHSV=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])
    
    myMask=cv2.inRange(frameHSV, lowerBound, upperBound)
    #myMask=cv2.bitwise_not(myMask)
    myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))
    myObject=cv2.bitwise_and(frame, frame, mask=myMask)
    
    myObjectSmall=cv2.resize(myObject,(int(width/2),int(height/2)))
    contours,junk=cv2.findContours(myMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    
    if len(contours)>0:
        #print("hedef nesne tespit edildi")
        sayac=0
        #print(len(contours))
        contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
        cv2.drawContours(frame,contours,-1,(255,0,0),3)
        contour=contours[0]
        x,y,w,h=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)


        
        cx=int((x+x+w)/2)
        cy=int((y+y+h)/2)
        cv2.circle(frame,(cx,cy), 5 , (0,0,255), -1)
        cv2.circle(frame, (320, 240), 45, (0,0,255), 2)
        cv2.line(frame,(320,0),(320,480),(0,0,255),2)
        cv2.line(frame,(0,240),(640,240),(0,0,255),2)
        if (cx > 300 and cx < 340 and cy > 220 and cy < 260):
                print("Merkezde")
                axy=[orta_x,orta_y]
                fp=open("pay1.pkl","wb")
                pickle.dump(axy,fp,protocol=2)
                fp.close()
        if cx<320:
            if cy<240:
                #print("hedef ekranın sol üstünde")
                axy=[cx,cy]
                #print("koordinatlar: " , axy)
                
                fp=open("pay1.pkl","wb")
                pickle.dump(axy,fp,protocol=2)
                fp.close()
                
            else:            
                #print("hedef ekranın sol altında")
                axy=[cx,cy]
                #print("koordinatlar: " , axy)
                
                fp=open("pay1.pkl","wb")
                pickle.dump(axy,fp,protocol=2)
                fp.close()
                
        if cx>320:
            if cy<240:
                #print("hedef ekranın sağ üstünde")
                axy=[cx,cy]
                #print("koordinatlar: " , axy)
                
                fp=open("pay1.pkl","wb")
                pickle.dump(axy,fp,protocol=2)
                fp.close()
                
            else:                
                #print("hedef ekranın sağ altında")
                axy=[cx,cy]
                #print("koordinatlar: " , axy)
                
                fp=open("pay1.pkl","wb")
                pickle.dump(axy,fp,protocol=2)
                fp.close()
                
    
    if len(contours)<2:
        axy=[orta_x,orta_y]
        fp=open("pay1.pkl","wb")
        pickle.dump(axy,fp,protocol=2)
        fp.close()
        #print("ekranda hiçbir hedef yok")
        sayac=sayac+1
        print("hedefin algılanması bekleniyor sayac=", sayac)
        if sayac==250:
            break
        
        
    #cv2.imshow("my object", myObjectSmall)
    #cv2.moveWindow("my object", int(width/2), int(height))
    #cv2.imshow("maskelenmiş görüntü", myMaskSmall)
    #cv2.moveWindow("maskelenmiş görüntü", 0, height)
    #cv2.imshow('orijinal görüntü', frame)
    #cv2.moveWindow('orijinal görüntü',0,0)
    
    
    
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()






























