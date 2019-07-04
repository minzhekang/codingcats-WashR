#!/usr/local/bin/python

import RPi.GPIO as GPIO
import datetime
import time
import matplotlib.pyplot as plt
from libdw import pyrebase

url = 'https://week4-raspberry-pi.firebaseio.com/'  # URL to Firebase database
apikey = '-'
config = {
    "apiKey": apikey,
    "databaseURL": url,
    "authDomain": "week4-raspberry-pi.firebaseapp.com",
    "storageBucket": "week4-raspberry-pi.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

GPIO.setmode(GPIO.BOARD)

# define the pin that goes to the circuit
pin_to_circuit = 7

datacollect=[]
today={}
cumall=dict(db.child("W1/logger").get().val())

def rc_time (pin_to_circuit):
    count = 0
    # make cumall a global variable so it can be obtained from outside the function
    global cumall
    global today
    # Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)


    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    # Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
    if count!= 0:
        state="no light"
        currenttime=datetime.datetime.now().strftime("%H%M") # 24 hour format
        currentset=(currenttime,0)
        if len(datacollect)>0:  
            if datacollect[len(datacollect)-1][1]==1:   # checks if the current state is different from previous readings
                datacollect.append(currentset)
                today[currenttime]=0
                try:
                    db.child("W1/On").set(0)  # append to firebase the current state of washing machine
                finally:
                    pass

        if len(datacollect)==0:
            datacollect.append(currentset)
            today[currenttime]=0
            try:
                db.child("W1/On").set(0)  # append to firebase the current state of washing machine if no data
            finally:
                pass

               
    else:
        state="light detected"
        currenttime=datetime.datetime.now().strftime("%H%M") # 24 hour format
        currentset=(currenttime,1)
        if len(datacollect)>0:
            if datacollect[len(datacollect)-1][1]==0: # checks if the current state is different from previous readings
                datacollect.append(currentset)
                today[currenttime]=1
                try:
                    db.child("W1/On").set(1) # append to firebase the current state of washing machine
                finally:
                    pass


        if len(datacollect)==0:
                datacollect.append(currentset)
                today[currenttime]=1
                try:
                    db.child("W1/On").set(1)  # append to firebase the current state of washing machine if no data collect
                finally:
                    pass


    if int(currenttime) == 0: # reset time @ midnight int("0000") == 0
         
        cumall={k: today.get(k,0) + cumall.get(k,0) for k in set(today) | set(cumall)} # combines cumulative data obtained from previous days with today's data
        today={} # resets today's data ( to prevent excessive app ram usage )
    
        try:
            db.child("W1/logger").set([(a,b) for a,b in cumall.items()]) # updates cumulative data to firebase at 12am
        finally:
            pass
    time.sleep(1)
    return count


#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    while True:
        rc_time(pin_to_circuit) # Keeps the code running forever
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    
