import cv2
import numpy as np
import time
import serial
ser = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

cap = cv2.VideoCapture(0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0
while (True):
    ret, frame = cap.read()
    frame_id += 1
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
      for detection in out: 
          scores = detection[5:]
          class_id = np.argmax(scores)
          confidence = scores[class_id]
          if confidence > 0.2:
             # Object detected
             center_x = int(detection[0] * width)
             center_y = int(detection[1] * height)
             w = int(detection[2] * width)
             h = int(detection[3] * height)
             # Rectangle coordinates
             x = int(center_x - w / 2)
             y = int(center_y - h / 2)
             boxes.append([x, y, w, h])
             confidences.append(float(confidence))
             class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)
    for i in range(len(boxes)):
      if i in indexes:
         x, y, w, h = boxes[i]
         label1 = str(classes[class_ids[i]])
         confidence = confidences[i]
         color = colors[class_ids[i]]
         cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
         cv2.rectangle(frame, (x, y), (x + w, y + 30), color, -1)
         cv2.putText(frame, label1 + " " + str(round(confidence, 2)), (x, y + 30), font, 2, (255, 255, 255), 2)
##         print("label 1:",label1)
##    for i in range(len(boxes)):
##      if i in indexes:
##         x, y, w, h = boxes[i]
##         label2= str(classes[class_ids[i]])
##         confidence = confidences[i]
##         color = colors[class_ids[i]]
##         cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
##         cv2.rectangle(frame, (x, y), (x + w, y + 30), color, -1)
##         cv2.putText(frame, label2 + " " + str(round(confidence, 2)), (x, y + 30), font, 2, (255, 255, 255), 2)
##         print("label 2:",label2)
         if label1 == "elephant"  or label1 =="bear" or label1 =="zebra" or label1 =="giraffe":
             print(label1)
##             print(label2)
             num = "wild" # Taking input from user
             print("Higher buzzer alert")
             ser.write(num.encode())
             print(num)
             time.sleep(1)
             
##             
##             
##             
         elif label1 == "bird" or label1 == "sheep" or label1 == "dog" or label1 == "cat" or label1 == "cow":
             print(label1)
             
##             
    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 2, (0, 0, 0), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
cap.release()
cv2.destroyAllWindows()