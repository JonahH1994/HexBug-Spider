import socket
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
import functions_tcp
#import ViconTrackerPoseHandler

TCP_IP = '192.168.137.101'
TCP_PORT = 80
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

tolerance = 0.5

def isAtLoc( p1, p2, tol ):

	p = cordToRad( p1, p2 )

	if np.abs( p ) < tol:
		return 1
	else:
		return 0

def cordToRad( p1, p2, the = None ):

	if the is None:

		r12 = p2 - p1 

		r = np.sqrt( np.dot( r12, r12 ) )

		return r

	else:

		r12 = p2 - p1 
		nor = [ np.cos(the), np.sin(the) ]

		r = np.sqrt( np.dot( r12, r12 ) )
		theN = np.arccos( np.dot( nor, r12 )/ r )


		# Check to see if angle should be positive or negative
		nor1 = [ np.cos( the + theN ), np.sin( the + theN ) ]

		print( np.abs( np.dot( nor1, r12 )/ r - 1 ) )

		if( np.abs( np.dot( nor1, r12 )/ r - 1) > tolerance ):
			theN = -theN 

		return r, theN


# axis dimension
dim = 30

x = 0
y = 0
pos = []

x0 = 0 ;
y0 = 0 ;
the0 = np.pi/2

plt.ylim( -(dim+1), (dim+1) )
plt.xlim( -(dim+1), (dim+1) )
plt.grid()
pos = plt.ginput( 0,0 )
plt.close()

pos = np.array( [pos] ) 
pos = pos[ : ][ 0 ]

x_cord = pos[ :, 0 ]
y_cord = pos[ :, 1 ] 

dm = len(pos)

r = np.zeros(dm)
thes = np.zeros( dm )
labels = np.zeros( dm )

for i in range(dm):

	if i is 0:

		r[i], thes[i] = cordToRad( [x0,y0], pos[i], the0 )

	else:

		r[i], thes[i] = cordToRad( pos[i-1], pos[i], the0 )

	the0 += thes[i]
	labels[i] = i + 1

print( "Radius: " )
print( r ) 
print( "Thetas: " )
print( thes )

#'''
plt.figure(1)
plt.ion() 
plt.plot( x_cord, y_cord, 'o' )
plt.ylim( -(dim+1), (dim+1) )
plt.xlim( -(dim+1), (dim+1) )
plt.grid()
#plt.annotate( labels )

i = 0
for xy in zip( x_cord, y_cord ):

	plt.annotate('(%s)' % labels[i], xy=xy, textcoords='data')
	i += 1

plt.show() 
#'''

functions_tcp.writeToTCP( r, thes, s )

s.send(b's')

s.close()

input(  "Motion has ended. Press enter to continue: " )
 # print "received data:", data