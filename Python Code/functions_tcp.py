import numpy as np
import sys
import socket
import time

rot_const = 3 / 2/ np.pi
mot_const = 3.69 

# To move forward: "i"
# To move backward: "k"
# To move right: "l"
# To move left: "j"

def writeToTCP( r, the, ser ):

	for i in range(len(r)): 

		if( the[i] == 0 ):
		
			fwd_back( r[i], ser )

		else:

			rig_lef( the[i], ser ) 
			fwd_back( r[i], ser )

	#ser.write( b"s")
	#ser.sendto( b"s", (UDP_IP, UDP_PORT) )


def fwd_back( r, ser ):

	if r < 0:

		#ser.write( b"k")
		#ser.sendto( b"k", (UDP_IP, UDP_PORT) )
		ser.send( b'k' ) 

	else:

		#ser.write( b"i")
		#ser.sendto( b"i", (UDP_IP, UDP_PORT) )
		ser.send( b'i')

	time.sleep( np.abs( r/ mot_const ) )
	#ser.sendto( b"s", (UDP_IP, UDP_PORT) )

def rig_lef( the, ser ):


	if the < 0:

		#ser.write( b"l")
		#ser.sendto( b"l", (UDP_IP, UDP_PORT) )
		ser.send( b'l' )

	else:

		#ser.write( b"j")
		#ser.sendto( b"j", (UDP_IP, UDP_PORT) )
		ser.send( b'j' )

	time.sleep( np.abs( the * rot_const ) )
	#ser.sendto( b"s", (UDP_IP, UDP_PORT) )
	ser.send( b's' )
	time.sleep(1)