import RPi.GPIO as GPIO
from time import sleep
import cv2


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

try:
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        body = body_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) + len(body) > 0:
            GPIO.output(18, 1)
            sleep(0.1)
            GPIO.output(18, 0)
            sleep(0.1)

finally:
    GPIO.cleanup()
