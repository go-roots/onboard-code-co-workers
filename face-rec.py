# Import the libraries
import face_recognition
import picamera
import numpy as np
import time
import requests
#Setup the Camera
camera = picamera.PiCamera()
camera.resolution = (320, 240)
# Initialize some variables
face_locations = []
print("Capturing image.")
#Program Loop
while True:
    #Take a picture
    camera.capture('output.jpg')
    #Load the image using 
    output = face_recognition.load_image_file('output.jpg')
    #Cherche for faces
    face_locations = face_recognition.face_locations(output)
    #If faces send the image to the WebService for face recognition
    if len(face_locations) > 0:
        print("Found a face sending image")
        #The room of the Raspberry is harcoded in the query
        endpoint = "http://206.189.55.55/?room=room%201" 
        r = requests.post(endpoint, files={'file':open("output.jpg",'rb')})
        #Wait for 2 seconde to not spam the same picture
        time.sleep(2)