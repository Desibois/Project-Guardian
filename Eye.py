import numpy as np
import cv2

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
coordinates = [0, 0]

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape

    max_height = 6/10 * height
    min_height = 4/10 * height
    max_width = 6/10 * width
    min_width = 4/10 * width

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
    if len(faces) > 0:
        print("IN FRAME")
        for x, y, w, h in faces:
            coordinates[0] = x
            coordinates[1] = y          
    elif coordinates[0] == 0 and coordinates[1] == 0:
        pass

    elif coordinates[0] < min_width:
        print("Move left")
        coordinates = [0, 0]

    elif coordinates[0] > max_width:
        print("Move right")
        coordinates = [0, 0]
    
    if len(faces) > 0:
        print("IN FRAME")
        for x, y, w, h in faces:
            coordinates[0] = x
            coordinates[1] = y  
                    
    elif coordinates[0] == 0 and coordinates[1] == 0:
        pass

    elif coordinates[1] < min_height:
        print("Move down")
        coordinates = [0, 0]
        
    elif coordinates[1] > max_height:
        print("Move up")
        coordinates = [0, 0]
    

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord("j"):
        break

cap.release()
