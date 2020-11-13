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

