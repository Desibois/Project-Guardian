import face_recognition
import cv2
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

ref_image = face_recognition.load_image_file("ref.png")
ref_encoding = face_recognition.face_encodings(ref_image)[0]

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    intruder_detected = False

    for face_encoding in face_encodings:
        match = face_recognition.compare_faces([ref_encoding], face_encoding)

        if not match[0]:
            intruder_detected = True
            break

    if intruder_detected:
        GPIO.output(18, 1)  
        print("fire")
        sleep(1)
        GPIO.output(18, 0) 
    else:
        print("don't fire")  

video_capture.release()
GPIO.cleanup()
