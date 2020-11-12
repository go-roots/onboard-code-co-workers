import requests
import json
import serial

import RPi.GPIO as GPIO
import time
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)


urlgetRedeemable = "https://co-workers.herokuapp.com/api/cw-api/redeemables/"
urlpostcreate = "https://co-workers.herokuapp.com/api/cw-api/transactions"
urlpostval = "https://co-workers.herokuapp.com/api/cw-api/transactions/validate"

PortRF = serial.Serial('/dev/ttyAMA0',9600)

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVkN2E1MTRiNWQyYzEyYzc0NDliZTA0MiIsImlhdCI6MTYwNDk1NjM3MiwiZXhwIjoxNjEwMTQwMzcyfQ.IuVY6TnFi1EKN7J4aMNbuP4yH7fY5_krDFiWIiJ2mQg"

def chooseRedeemable():
    r = requests.get(urlgetRedeemable, headers={'Authorization': 'Bearer ' + TOKEN})
    redeems = r.json()
    for i in range(0, len(redeems)):
        print(i , " : " , redeems[i]['name'] , " Description: " , redeems[i]['description'] , " Price: " , redeems[i]['price'] , " CWPs")
    
    x = int(raw_input("Type the number of your command: "))
    redeemId = redeems[x]['_id']
    redeemItem = redeems[x]['name']
    return redeemId, redeemItem

def scanTheCard():
    print("Light:")
    GPIO.output(23, GPIO.HIGH)
    print("T:")
    while True:
        print("...")
        ID = ""
        read_byte = PortRF.read()
        if read_byte=="\x02":
            for Counter in range(0,12):
                print("...2")
                read_byte=PortRF.read()
                ID = ID + str(read_byte)
            return ID


def doTransaction(redeemable, rfid):
    r = requests.post(urlpostcreate, headers={'Authorization': 'Bearer ' + TOKEN}, json={'redeemableId': redeemable})
    trans = r.json()
    GPIO.output(23, GPIO.LOW)
    return trans['data']['transaction']


def validateTransaction(idTransaction, redeemItem, rfid):
    r = requests.post(urlpostval, headers={'Authorization': 'Bearer ' + TOKEN}, json={'transactionId': idTransaction, 'redeemable': redeemItem, 'rfid':rfid})
    res = r.json()
    print(res)
    if(res['success']== False):
        print("blink")
        blinkError()
        return False
    return res['success']


def blinkError():
    for i in range (0,3):
        GPIO.output(23, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(23, GPIO.LOW)
        time.sleep(0.1)


while True:
    redeemableId, redeemItem = chooseRedeemable()
    rfid = scanTheCard()
    idTransaction = doTransaction(redeemableId, rfid)
    rep = validateTransaction(idTransaction, redeemItem, rfid)
    if(rep == 'False'):
        blinkError()


