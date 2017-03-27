import numpy as np
import sys
import serial
import time

ser = serial.Serial('COM5', 9600) 

time.sleep(2)

# Time for one revolution is 3

tim = 3 ;
timT = 3/4 ;

#a = ser.write(b"j")
ser.flush() 

# build a square

ser.write(b"i") 
time.sleep(tim)

ser.write(b"j")
time.sleep(timT)

ser.write(b"i")
time.sleep(tim)

ser.write(b"j")
time.sleep(timT)

ser.write(b"i")
time.sleep(tim)

ser.write(b"j")
time.sleep(timT)

ser.write(b"i")
time.sleep(tim)

ser.write(b"j")
time.sleep(timT)

ser.write(b"s")

ser.close() 