import speech_recognition as sr
import threading
from time import sleep
import RPi.GPIO as GPIO

passed = False
verified = False
lock = threading.Lock()

def verify(command):
    global passed, verified
    with lock:
        if command == "vanguard":
            print("Ready to fire")
            verified = True
            passed = False
        elif command == "fire" and verified:
            print("Fire")
            passed = True
        elif command == "stop":
            passed = False
            verified = False
            print("Task Completed")

def fire():
    global passed
    while True:
        with lock:
            if passed:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(18, GPIO.OUT)
                GPIO.output(18, 1)
                sleep(0.1)
                GPIO.output(18, 0)
                sleep(0.1)
                print("FIRING")

listener = sr.Recognizer()

fire_thread = threading.Thread(target=fire, daemon=True)
fire_thread.start()

while True:
    try:
        with sr.Microphone() as mic:
            listener.adjust_for_ambient_noise(mic, duration=0.2)
            audio = listener.listen(mic)
            text = listener.recognize_google(audio)
            text = text.lower()
            verify_thread = threading.Thread(target=verify, args=(text,))
            verify_thread.start()
    except sr.UnknownValueError:
        listener = sr.Recognizer()
        continue
