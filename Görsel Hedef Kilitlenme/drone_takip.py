import cv2
import numpy as np
import time
import pid
import pyfirmata
from time import sleep
from threading import Thread

port = "COM16"
board = pyfirmata.Arduino(port)
servo_dikey = board.get_pin('d:9:s') # pin 9 Arduino
servo_yatay = board.get_pin('d:10:s') # pin 10 Arduino
minAngle, maxAngle = 30, 160
servoYatay=90
servoDikey=90
fark=3
# Opencv DNN
#net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
net = cv2.dnn.readNet("model/yolov4-tiny-obj_best.weights", "model/yolov4-tiny-obj.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255)

# Load class lists
classes = []
with open("model/classes.txt", "r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)


# Initialize camera
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("iha.mp4")



cap.set(cv2.CAP_PROP_FRAME_WIDTH, 920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# FULL HD 1920 x 1080


# Create window
cv2.namedWindow("Frame")

#Ekran Merkezi Dosyaya Yazılır
ekran_orta_x=int(640/2)
ekran_orta_y=int(480/2)
aci_hesapla = pid.pidss(ekran_orta_x,ekran_orta_y)
yatay_aci=aci_hesapla[0]
dikey_aci=aci_hesapla[1]
#servoYatay = np.interp(yatay_aci, [-0.78, 0.78], [minAngle, maxAngle])
#servoDikey = np.interp(dikey_aci, [-0.78, 0.78], [minAngle, maxAngle])
servo_yatay.write(servoYatay)
servo_dikey.write(servoDikey)
time.sleep(0.1)
#5 sn ara ile resim alma
def startLogger():
    while True:
        function()
        sleep(5)

def function():
    #print("save")
    camera = cv2.VideoCapture(0)
    _, img = cap.read()
    t = time.localtime(time.time())
    
    cv2.imwrite(f'resim/{t.tm_year}-{t.tm_mon}-{t.tm_mday}-{t.tm_hour}-{t.tm_min}-{t.tm_sec}.jpg',img)#Kaydet

Thread(target=startLogger).start()
    
while True:
    # Get frames
    ret, frame = cap.read()
    frame=cv2.flip(frame,1)
    # Object Detection
    (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.3, nmsThreshold=.4)
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        (x, y, w, h) = bbox
        class_name = classes[class_id[0]]
        
        if class_name == "iha":
        
            cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,250), 2)
           
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,250), 3)
            hedef_x=int(2*bbox[0]+bbox[2])/2
            hedef_y=int(2*bbox[1]+bbox[3])/2
            print(hedef_x,hedef_y)
            aci_hesapla = pid.pidss(hedef_x,hedef_y)
            
            yatay_aci=aci_hesapla[0]
            dikey_aci=aci_hesapla[1]
            #servoYatay = np.interp(yatay_aci, [-0.78, 0.78], [minAngle, maxAngle])
            #servoDikey= np.interp(dikey_aci, [-0.78, 0.78], [minAngle, maxAngle])
            
            print(servoYatay,servoDikey)
            if (hedef_x > 300 and hedef_x < 340 and hedef_y > 220 and hedef_y < 260):
                print("Merkezde")
                
                #servo_yatay.write(servoYatay)
                #servo_dikey.write(servoDikey)

            elif (hedef_x > 340 and hedef_x <640 ):
                if (hedef_y>10 and hedef_y<220):
                    print (" kuzey dogu ")
                    #servoYatay_1=95-servoYatay_1
                    #servoDikey_1=95-servoDikey_1
                    #servoYatay-= servoYatay_1
                    #servoDikey-= servoDikey_1
                    servoYatay+= fark
                    servoDikey+= fark
                    servo_yatay.write(servoYatay)
                    servo_dikey.write(servoDikey)
                    
                    
                elif(hedef_y>260 and hedef_y<480):
                    print (" guney dogu ")
                    servoYatay+= fark
                    servoDikey-= fark
                    servo_yatay.write(servoYatay)
                    servo_dikey.write(servoDikey)
                    
                    
            elif(hedef_x>5 and hedef_x < 300):
                if (hedef_y>5 and hedef_y<220):
                    print (" kuzey bati ")
                    servoYatay-= fark
                    servoDikey+= fark
                    servo_yatay.write(servoYatay)
                    servo_dikey.write(servoDikey)
                    
                    
                elif (hedef_y>260 and hedef_y<480):
                    print (" guney bati ")
                    servoYatay-= fark
                    servoDikey-= fark
                    servo_yatay.write(servoYatay)
                    servo_dikey.write(servoDikey)


    #Screen Divide
    cv2.circle(frame, (320, 240), 45, (0,0,255), 2)
    cv2.line(frame,(320,0),(320,640),(25,1,0),2)
    cv2.line(frame,(0,240),(640,240),(25,1,0),2)
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        aci_hesapla = pid.pidss(ekran_orta_x,ekran_orta_y)
        yatay_aci=aci_hesapla[0]
        dikey_aci=aci_hesapla[1]
        servoYatay = np.interp(yatay_aci, [-0.78, 0.78], [minAngle, maxAngle])
        servoDikey = np.interp(dikey_aci, [-0.78, 0.78], [minAngle, maxAngle])
        servo_yatay.write(servoYatay)
        servo_dikey.write(servoDikey)
        
        time.sleep(0.5)
        break

    
#prog. end
cap.release()
cv2.destroyAllWindows()
