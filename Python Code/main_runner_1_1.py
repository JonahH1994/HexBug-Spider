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

path1 = r"C:\Users\Jonah\OneDrive - Cornell University\Summer 2017\Research\Bot Trajectories\ "

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

if len( hexBugs ) > 1:

	for i in range( len(hexBugs) ):

		for j in range( len(hexBugs) ):

			if i != j:
				hexBugs[i].bots.append( hexBugs[j] )

# axis dimension
dim = 2

#define HexBug1:
#vic_port = 51001
#hb1 = hx.hexBug( UDP_IP, 'HexBug1', UDP_PORT, vic_port )

time.sleep(3)
pos = []
labels = []
a=[]

p = 1 
j = 1

"""
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
"""

plt.ylim( -dim, dim )
plt.xlim( -dim, dim )
plt.grid()

plt.plot( x, y, '*' )
p = plt.ginput(0,0)

plt.close()

print( p ) 

"""
p =  np.concatenate( p, axis=0 )
print( 'array after concatenate: ' )
print( p )

p.reshape(-1)
print( 'array after reshape' )
print( p )
"""

pos = p

"""
pos = np.concatenate(pos, axis=0)
print( 'array after concatinating again' ) 
print( pos )
"""
#labels = np.concatenate( labels, axis=0 )

#x_cord = np.zeros( int( len( pos )/ 2 )) 
#y_cord = np.zeros( int( len( pos )/ 2 )) 
x_cord = []
y_cord = []
#pose = np.zeros( int( len( pos )/ 2 )) 
pose=[]

print( len(pos) )

for m in range( len( pos ) ):

	x_cord.append( pos[m][0] )
	y_cord.append( pos[m][1] )
	pose.append( [pos[m][0],pos[m][1]] )

print( 'array post processing' )
print( pose )
for l in range( n ):

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

	time.sleep(1)
	ray = []
	for i in range( len(hexBugs) ):
		ray.append( hexBugs[i].r0[0:2] )

	if len(hexBugs) > 1:
		ray = np.concatenate(ray, axis=0)
	array.append( hexBugs[0].r0[0:2] )

print( "Final Destination: " + str( hexBugs[0].r0[0:2] ) )

f = open( path1 + 'hexBugTraj_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.csv', 'w',  newline='')

try:

    print( 'Writing trajectory to a file.' )

    writer = csv.writer(f, delimiter=',')
    labs = []
    for i in range( len( hexBugs ) ):
    	labs.append( ["X Position", "Y Position"] )

    labs = np.concatenate(labs, axis=0)
    writer.writerow( labs )
    for i in range( len(array) ):
    	writer.writerow(array[i])

    print('Done writing.' )
    
except Exception as ex:

	print( type(ex) )
	print( ex )

finally:
    f.close()

input(  "Motion has ended. Press enter to continue: " )
sys.exit()