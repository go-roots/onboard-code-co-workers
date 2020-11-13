# Import the used libraries
import requests
import json
import serial
import RPi.GPIO as GPIO
import time

#Clean the possible used GPIO Port
GPIO.cleanup()

#Setup the Led
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

#The URLS Used during the code
urlgetRedeemable = "https://co-workers.herokuapp.com/api/cw-api/redeemables/"
urlpostcreate = "https://co-workers.herokuapp.com/api/cw-api/transactions"
urlpostval = "https://co-workers.herokuapp.com/api/cw-api/transactions/validate"

PortRF = serial.Serial('/dev/ttyAMA0',9600)

#Admin Token used for transaction
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVkN2E1MTRiNWQyYzEyYzc0NDliZTA0MiIsImlhdCI6MTYwNDk1NjM3MiwiZXhwIjoxNjEwMTQwMzcyfQ.IuVY6TnFi1EKN7J4aMNbuP4yH7fY5_krDFiWIiJ2mQg"

# Fetch and display the Redeemables
def chooseRedeemable():
    r = requests.get(urlgetRedeemable, headers={'Authorization': 'Bearer ' + TOKEN})
    redeems = r.json()
    #Display the redeemables
    for i in range(0, len(redeems)):
        print(i , " : " , redeems[i]['name'] , " Description: " , redeems[i]['description'] , " Price: " , redeems[i]['price'] , " CWPs")
    
    #Ask the user to choose his redeemables
    x = int(raw_input("Type the number of your command: "))
    redeemId = redeems[x]['_id']
    redeemItem = redeems[x]['name']
    return redeemId, redeemItem

def scanTheCard():
    #Turn on the light
    GPIO.output(23, GPIO.HIGH)

    #Wait for the User to scan his card
    while True:
        ID = ""
        read_byte = PortRF.read()
        if read_byte=="\x02":
            for Counter in range(0,12):
                print("...2")
                read_byte=PortRF.read()
                ID = ID + str(read_byte)
            return ID


#Prepare the transaction and turn down the light
def doTransaction(redeemable, rfid):
    r = requests.post(urlpostcreate, headers={'Authorization': 'Bearer ' + TOKEN}, json={'redeemableId': redeemable})
    trans = r.json()
    GPIO.output(23, GPIO.LOW)
    return trans['data']['transaction']


#Send the validation request 
def validateTransaction(idTransaction, redeemItem, rfid):
    r = requests.post(urlpostval, headers={'Authorization': 'Bearer ' + TOKEN}, json={'transactionId': idTransaction, 'redeemable': redeemItem, 'rfid':rfid})
    res = r.json()
    print(res)
    if(res['success']== False):
        print("blink")
        blinkError()
        return False
    return res['success']

#Code that handle the blinking of the light when a error occur
def blinkError():
    for i in range (0,3):
        GPIO.output(23, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(23, GPIO.LOW)
        time.sleep(0.1)


#Loop of the program
while True:
    redeemableId, redeemItem = chooseRedeemable()
    rfid = scanTheCard()
    idTransaction = doTransaction(redeemableId, rfid)
    rep = validateTransaction(idTransaction, redeemItem, rfid)
    if(rep == 'False'):
        blinkError()


