import cv2
import numpy as np
import time
import matplotlib.pyplot as plt



class Detecter():
    def __init__(self):
        # Opencv DNN
        net = cv2.dnn.readNet("./custom-yolov4-tiny-detector_best.weights", "./custom-yolov4-tiny-detector.cfg")
        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(320, 320), scale=1/255)


        # Load class lists
        classes = []
        with open("./classes.txt", "r") as file_object:
            for class_name in file_object.readlines():
                #print(class_name)
                class_name = class_name.strip()  

                classes.append(class_name)

        check=0
        count=0
        # plt.figure()
        # Initialize camera
        cap = cv2.VideoCapture(0)


        while True:
        # Get frames
            ret, frame = cap.read()

            blank=np.zeros(frame.shape[:2],dtype='uint8')

            # Object Detection
            (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.3, nmsThreshold=.4)
            for class_id, score, bbox in zip(class_ids, scores, bboxes):
                (x, y, w, h) = bbox
                cv2.rectangle(frame, (x, y), (x + w, y + h), (200,0,50), 3)
                count=count+1

                class_name = classes[class_id]

                # cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 3, (200,0,50), 2)

                mask=cv2.rectangle(blank, (x, y), (x + w, y + h), 255, -1)

                masked=cv2.bitwise_and(frame,frame,mask=mask)
                gray=cv2.cvtColor(masked,cv2.COLOR_BGR2GRAY)
                gray_hist=cv2.calcHist([gray],[0],None,[256],[0,256])
                # plt.clf()
                # plt.plot(gray_hist)
                # plt.xlim([0,256])
                # plt.draw()
                # plt.show() 


                if self.getColor(x,y,w,h,frame):
                
                    cv2.putText(frame, "Uzunlar Yandi", (x+20, y +20), cv2.FONT_HERSHEY_PLAIN, 3, (200,0,50), 2)




            # if count==check:
            #     cv2.imshow("Frame", frame)
            #     key = cv2.waitKey(1)

            # else:
            cv2.imshow("Frame",frame)
                # check=count
            key = cv2.waitKey(1)

            if key == 27:
                break

    def getColor(self,x,y,w,h,frame):
            cropped_img = frame[y:y+h, x:x+w]
            gray=cv2.cvtColor(cropped_img,cv2.COLOR_BGR2GRAY)
            gray_hist=cv2.calcHist([gray],[0],None,[256],[0,256])
            top=max(gray_hist)
            for x,y in enumerate(gray_hist):
                if gray_hist[x]==top:
                    index=x
                    break
            if index <150:
                return False
            else: 
                return True
            # white=[]
            # black=[]
            # for val in gray_hist:
            #     if val<150:
            #         black.append(val)
            #     else:
            #         white.append(val)
            
            # if sum(white)>sum(black):
            #     return True
            # else:
            #     return False

            # cap.release()
            # cv2.destroyAllWindows()

Detecter()