#save data in a file on desktop

import RPi.GPIO as GPIO
import datetime
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Initialize instance variables
SCK = 23
CS = 24
SO = 21
T0 = 33
T1 = 31
T2 = 29

# Setup all of the GPIO pins
GPIO.setup(SCK, GPIO.OUT)
GPIO.setup(T0, GPIO.OUT)
GPIO.setup(T1, GPIO.OUT)
GPIO.setup(T2, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)
GPIO.setup(SO, GPIO.IN)

# Infinite loop
while True:
    
    #initialize reading
    Reading0 = 0.0
    Reading1 = 0.0
    Reading2 = 0.0
    Reading3 = 0.0
    Reading4 = 0.0
    Reading5 = 0.0
    Reading6 = 0.0
    Reading7 = 0.0
    
    # make a time stamp
    ct = datetime.datetime.now()

    # Initialize all of the GPIO pins
    GPIO.output(SCK, 0)
    GPIO.output(T0, 0)
    GPIO.output(T1, 0)
    GPIO.output(T2, 0)
    GPIO.output(CS, 1)

    # Initialize the poll data to zero
    latestdata = 0b0

    # Select the thermocouple using multiplexer
    for thermID in range(8):
        GPIO.output(T2, thermID & 0b100)
        GPIO.output(T1, thermID & 0b10)
        GPIO.output(T0, thermID & 0b1)

    # Wait for the multiplexer to update
        sleep(1)
        
    # Select the chip and record incoming data
        data = 0b0
        data2 = 0b0
        dataf = 0.0
    
        GPIO.output(CS, 0)

    # Shift in 32 bits of data
        for bitshift in reversed(range(32)):   #31, 30, ... to 0 (total 32 numbers)
            GPIO.output(SCK, 1)
            data += GPIO.input(SO) << bitshift
            GPIO.output(SCK, 0)
        GPIO.output(CS, 1)
        latestdata = data

        data2 = latestdata
    # Select appropriate bits
        data2 = data2 >> 18
    # Handle twos complement
        if data2 >= 0x2000:
            data2 = -((data2 ^ 0x3fff) + 1)
    # Multiplied by 0.25 to show the decimal component
        dataf = 0.25*data2

        if (thermID == 0):
            Reading0 = dataf
            
        if (thermID == 1):
            Reading1 = dataf

        if (thermID == 2):
            Reading2 = dataf

        if (thermID == 3):
            Reading3 = dataf

        if (thermID == 4):
            Reading4 = dataf

        if (thermID == 5):
            Reading5 = dataf

        if (thermID == 6):
            Reading6 = dataf

        if (thermID == 7):
            Reading7 = dataf
        
    filehandle = open('compost_temp_8channels.txt','a')  #it can also create a new file. 'a' is for append.
    filehandle.write("\n" + "%s" % ct) # %s is replaced by the variable ct.
    filehandle.write(" %s" % Reading0)
    filehandle.write(" %s" % Reading1)
    filehandle.write(" %s" % Reading2)
    filehandle.write(" %s" % Reading3)
    filehandle.write(" %s" % Reading4)
    filehandle.write(" %s" % Reading5)
    filehandle.write(" %s" % Reading6)
    filehandle.write(" %s" % Reading7)
    filehandle.close()  #without closing, file will not be saved automatically.
    sleep(5)