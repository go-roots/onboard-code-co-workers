# The code used in the Raspberry Pi Sensor
The face-rec.py file contain the code Camera sensor used to track the users position  
The rfid.py file contain the code used for the redeeming using RFID  

The followings explanation are the leaflet for our IoT Projects

## RFID - Project 1
By Ilja and Jorgo  

The redeeming of an item is processed with the following algorithm 
![alt schema](https://user-images.githubusercontent.com/63868715/99004574-9ea96100-253f-11eb-8ad6-36e6fcf5f5f8.png)
  
1- The User start by selecting the redeemable he want to buy. The redeemables are fetched using the Co-Workers API  
2- A Transaction for this item is created by making a request on the API. The API answer and if the transaction fail the led Blink in quick sucession to indicate the error. If the transaction is accepted the light turn on and the user can scan his RFID Card.   
3- The user scan his card.   
4- The ID of the card is linked to the transaction and the transaction is send to the API to be validated if the transaction fail the led Blink in quick sucession to indicate the error. If the transaction suceed the light stop blinking   
5- The User enjoy his redeemable   


This project can be divided in two parts: API Side (Co-workers API) and Client Side (Raspberry Pi)   
  
### API Side - Transaction Security


### Client Side - Transaction Handling
On the client side the code can be considered as a POC, as for now the Redeemable is chosen directly on the computer and the giving of the redeemable is not yet defined.  
However the present code is the backbone of a safe and efficient redeeming.  

## Face-Recognition - Project 2
By Shraddha, DaiQiao and Paul

The face recognition work according to the following schema:  
![alt schema](https://user-images.githubusercontent.com/63868715/99015411-3e251e80-2555-11eb-9dbf-c1fd5ad40044.png)
The code in the Raspberry is only a small part of the face-recognition. As the Raspberry is not powerful enough to process in an optimized way the face-recognition, most of the processing is done in the WebService (https://github.com/go-roots/face-recognition-co-workers)   


As seen below the code in the raspberry is pretty self-explanatory: 
```python
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
```

