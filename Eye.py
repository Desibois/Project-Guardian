import numpy as np
import cv2

xlimit = 1.8
ylimit = 1.8

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
coordinates = [0, 0, 0, 0]

def face_centre(coordinates):
    x = coordinates[0]
    y = coordinates[1]
    w = coordinates[2]
    h = coordinates[3]
    centre_x = x + (w//2)
    centre_y = y + (h//2)
    return [centre_x, centre_y]
    
def calculate_move(face, centre):
    if face[0] > centre[0] * xlimit:
    	print('move left')
    elif face[0] < centre[0] * xlimit:
        print('move right')
    if face[1] > centre[1] * ylimit:
        print('move down')
    elif face[1] < centre[1] * ylimit:
        print('move up')

        
        
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    centre = [width//2, height//2]
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        print('in frame')
        coordinates = faces[0]
    elif coordinates[0] == 0 and coordinates[1] == 0:
        pass
    else:
        face = face_centre(coordinates)
        calculate_move(face, centre)
        face = [0, 0, 0, 0]
