import numpy as np
import sys
import serial
import time

ser = serial.Serial('COM5', 9600) 

time.sleep(2)

rot_const = 3 / 2/ np.pi

def fwd_back( f_b, f_b0 ):

	if( f_b < 0 ):
		print("Moving backward for ", f_b, "seconds" )
		ser.write( b"k")
		f_b0 = f_b 

	else:
		print("Moving Forward for ", f_b, "seconds" )
		ser.write( b"i")
		f_b0 = f_b 

	time.sleep(f_b)

def rig_lef( thet, the0 ):

	if( thet > 0 ):
		print("Turning right for ", (thet*rot_const), "seconds" )
		ser.write( b"l")
		thet0 = thet

	else:
		print( "Turn left for ", np.abs(thet*rot_const), "seconds" )
		ser.write( b"j")
		thet0 = thet

	time.sleep( np.abs( thet * rot_const ) )

#ser = serial.Serial('COM5', 9600) 

#time.sleep(2)

#a = np.array( input("Please enter the positions you'd like to move to (i.e. [[x1,y1],[x2,y2],..])") ).reshape(-1)

fwd = 'i' 
bak = 'k' 
rgt = 'l'
lef = 'j'

r0 = 0 
th0 = 0
prev_ang = 0

a = input("Please enter the positions you'd like to move to (i.e. r1 th1, r2 th2,...): ").split(",")
a = [ [ float(y) for y in x.split() ] for x in a ]

print( len(a) ) 
print( a[0])
i = 0 

while( i != len(a) ):

	r1, th1 = a[i] 

	if( th1 == 0 ):
		
		fwd_back( r1, r0 )

	else:

		rig_lef( th1, th0 ) 
		fwd_back( r1, r0 )

	i += 1

ser.write( b"s")