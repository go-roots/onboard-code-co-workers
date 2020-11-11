import face_recognition
import picamera
import numpy as np
import time
import requests

camera = picamera.PiCamera()
camera.resolution = (320, 240)
#output = np.empty((240, 320, 3), dtype=np.uint8)

# Initialize some variables
face_locations = []
print("Capturing image.")
while True:
    
    camera.capture('output.jpg')
    output = face_recognition.load_image_file('output.jpg')
    face_locations = face_recognition.face_locations(output)

    if len(face_locations) > 0:
        print("Found a face sending image")
        endpoint = "http://206.189.55.55/?room=room%201" 
        r = requests.post(endpoint, files={'file':open("output.jpg",'rb')})
        time.sleep(2)