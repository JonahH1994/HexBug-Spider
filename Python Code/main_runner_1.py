import socket
import numpy as np
import sys
import csv
import time
import matplotlib.pyplot as plt
import functions_tcp
import hexBug_1 as hx
import threading as td 
from datetime import datetime

def checkBugs( bugs ):

	l = len( bugs ) 
	motion = 0

	for i in range( l ):

		if bugs[i].motionStart == 1:
			motion = 1
			break 

	return motion 

vic_port = 0

n = int( input("How many robots will you be using? " ) )

hexBugs = []
x = []
y = []

for i in range(n):

	UDP_IP = input( ( "Enter the IP addres for Bot " + str(i+1) + ": " ) )
	UDP_PORT = int( input( ("Enter the port for Bot " + str(i+1) + ": ") ) )
	name = input( ("Enter the Vicon name for Bot " + str(i+1) + ": ") )	
	vic_port = int( input( ("Enter the Vicon port for Bot " + str(i+1) + ": ") ) )
	hexBugs.append( hx.hexBug( UDP_IP, name, UDP_PORT, vic_port ) )
	r = hexBugs[i].getPos()
	x.append( r[0] )
	y.append( r[1] )

# axis dimension
dim = 3

#define HexBug1:
#vic_port = 51001
#hb1 = hx.hexBug( UDP_IP, 'HexBug1', UDP_PORT, vic_port )

time.sleep(3)
pos = []
labels = []
a=[]

p = 1 
j = 1

while p != []:

	plt.ylim( -(dim+1), (dim+1) )
	plt.xlim( -(dim+1), (dim+1) )
	plt.grid()

	if j != 1:
		a = np.concatenate( pos, axis=0 )

		i = 0
		while i < len(a):

			plt.plot( a[i], a[i+1], 'o' )
			plt.annotate('(%s)' % labels[int(i/2)], xy=( a[i], a[i+1]), textcoords='data')
			i += 2

	plt.plot( x, y, '*' )
	p = plt.ginput( 0,0 )
	plt.close()

	if p == []:
		break 

	p = np.concatenate( p, axis=0)

	if len( p ) > 1:
		p.reshape(-1)

	if len(p)/2 == 1:

		labels.append( [j] )

	else:

		labels.append( np.ones(int( len(p)/2 ) ) * j )

	if j != 1:
		#labels = np.concatenate( labels, axis=0 )
		labels = labels 

	pos.append(p)
	j += 1


pos = np.concatenate(pos, axis=0)
print( pos )

labels = np.concatenate( labels, axis=0 )

x_cord = np.zeros( int( len( pos )/ 2 )) 
y_cord = np.zeros( int( len( pos )/ 2 )) 
#pose = np.zeros( int( len( pos )/ 2 )) 
pose=[]

for m in range( len( pos ) ):

	if m % 2 == 0:
		x_cord[int(m/2)] = pos[m]
		#pose[int(m/2)] = ( pos[m], pos[m+1] )
		pose.append( [pos[m],pos[m+1]] )

	else:
		y_cord[int((m+1)/2)-1] = pos[m] 

for l in range( n ):

	print( pose )
	hexBugs[l].writeXY( pose )

"""
plt.ion() 
plt.ylim( -(dim+1), (dim+1) )
plt.xlim( -(dim+1), (dim+1) )
fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.plot( x_cord, y_cord, 'o' )
ax.grid()
bot, = ax.plot( x, y, 'b*' )

i = 0
for xy in zip( x_cord, y_cord ):

	plt.annotate('(%s)' % labels[i], xy=xy, textcoords='data')
	i += 1

plt.show() 
"""


#plt.ion() 
"""
plt.figure(1)
plt.plot( x_cord, y_cord, 'o' )
plt.plot( x, y, 'b*' )
plt.ylim( -(dim+1), (dim+1) )
plt.xlim( -(dim+1), (dim+1) )
plt.grid()

i = 0
for xy in zip( x_cord, y_cord ):

	plt.annotate('(%s)' % labels[i], xy=xy, textcoords='data')
	i += 1

plt.show()
"""

array = []


#while hexBugs[0].motionStart == 1:
while checkBugs( hexBugs ) == 1:
	i = 0
	time.sleep(2)
	#print( hexBugs[0].r0 )
	#print( hexBugs[0].orientation )
	#bot.set_ydata( hexBugs[0].r0[1] )
	#bot.set_xdata( hexBugs[0].r0[0] )
	#print( "Previous Position: " + str( hexBugs[0].prevR[0:2] ) )
	#print( "Current Position: " + str( hexBugs[0].r0[0:2] ) )
	#print( "Final Destination: " + str( [x_cord,y_cord] ) )
	#fig.canvas.draw()
	array.append( hexBugs[0].r0[0:2] )

print( "Final Destination: " + str( [x_cord,y_cord] ) )

"""
f = open( 'hexBugTraj_' + str(datetime.now()) + '.csv', 'wt')

try:
    writer = csv.writer(f)
    writer.writerow( ('X position', 'Y Position') )
    print( 'Writing trajectory to a file.' )
    for i in range(len(array)):
        writer.writerow( array[i][0], array[i][1] )

    print('Done writing.' )
finally:
    f.close()
"""

input(  "Motion has ended. Press enter to continue: " )
#hb1.writeToTCP( r, thes )