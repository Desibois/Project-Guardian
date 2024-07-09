import threading
import cv2
import face_recognition as fr
import RPi.GPIO as GPIO
from time import sleep

cap = cv2.VideoCapture(0)
counter = 0
match = False
lock = threading.Lock()
ref_image = fr.load_image_file("ref.jpg")
ref_encoding = fr.face_encodings(ref_image)[0]
presence = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT) 


def check(frame):
    global match
    global presence
    face_locations = fr.face_locations(frame)
    face_encodings = fr.face_encodings(frame, face_locations)
    
    local_match = False
    for face_encoding in face_encodings:
        local_match = fr.compare_faces([ref_encoding], face_encoding)[0]
        if local_match:
            break
    
    with lock:
        if len(face_encodings) > 0:
            presence = True
        else:
            presence = False
        match = local_match

while True:
    ret, frame = cap.read()
    if ret:
        if counter % 15 == 0:
            try:
                threading.Thread(target=check, args=(frame.copy(),)).start()
            except ValueError as e:
                print(f"Thread error: {e}")
        counter += 1
        
        with lock:
            if presence:
                if match:
                    print("DON'T FIRE")
                else:
                    print("FIRE")
                    GPIO.output(18, 1)  
                    sleep(0.1)
                    GPIO.output(18, 0) 
            else:
                print("NO ONE DETECTED")
    else:
        print("Failed to capture frame")
