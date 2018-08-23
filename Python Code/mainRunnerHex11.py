import socket
import numpy as np
import sys
import csv
import time
import matplotlib.pyplot as plt
import functions_tcp
import rospy
import tf

import hexBugClass as hx
import threading as td 
from datetime import datetime

from collisionFreeDecentralized import *
import swarmParams
import updatedVicon as vt

import Sync2
import pathPlanning

def checkBugs( bugs ):

	l = len( bugs ) 
	motion = 0

	for i in range( l ):

		if bugs[i].motionStart == 1:
			motion = 1
			break 

	return motion

def updateDummies( dummy, ind, obj ):

	for i in range( len( dummy )):

			obj.currentPose[0:2,i] = np.matrix( dummy[i].getPose()[0:2] ).reshape((2,1))
		

m = 0

ip = input('Enter HexBug Number: ')

# HexBug IPs in order:
newIPs = [ '199.168.1.2', '199.168.1.148', '199.168.1.4', '199.168.1.5', '199.168.1.6', '199.168.1.7', '199.168.1.8', '199.168.1.11' ] # Not sure which one this is: 199.168.1.11 (Blue tagless)
IPs = [ newIPs[ip-1] ]

ports = [ 51010 ]

hexBugs = []
dummyBots = []
dummyBotsAndItself = []

x = []
y = []

UDP_PORT = 80s

n = len( IPs)

#high level controller
numOfGroups = 3 #2
loopingIndex = 2 #2

# Defines which regions each group moves to:
M1 = np.matrix([1, 2, 3, 2, 1])
M2 = np.matrix([2, 3, 2, 1, 2])
M3 = np.matrix([3, 2, 1, 2, 3])
autoMat = (M1,M2,M3)

# By setting this to all 1's, the hexbugs have to wait for each gropu to fully reach each region before moving on. To allow each group to continue with their task, set the corresponding 
# column equal to zero:
S1 = np.matrix([[1, 1, 1, 1, 1],[1, 1, 1, 1, 1],[1, 1, 1, 1, 1]])
S2 = np.matrix([[1, 1, 1, 1, 1],[1, 1, 1, 1, 1],[1, 1, 1, 1, 1]])
S3 = np.matrix([[1, 1, 1, 1, 1],[1, 1, 1, 1, 1],[1, 1, 1, 1, 1]])
syncMat = (S1,S2, S3)

# Define the region centers and the box that defines each region:
regionCenters = np.matrix([[-1.2,0,1.5],[0.6,0.6,0.6]])
offsetVector = np.matrix([[0.6,0.6,0.6],[0.6,0.6,0.6]]) 

# Initialize map and nodes:
MAP = pathPlanning.createMap()
nodes = pathPlanning.createNodes()

# Create an object for the specified HexBug:
hexBugs.append( hx.hexBug( IPs[0], 'HexBug' + str(ip), UDP_PORT, ip ) )
r = hexBugs[0].getPos()
x.append( r[0] )
y.append( r[1] )

vic_portF = 51010
vic_portL = 51017

Diff = 0
num = len(newIPs)

m= 0

for i in range(num):

	if i != ip-1:

		try:
			dum = vt.ViconTracker(i+1) # Create a vicon object for obstacle bot i+1:
			time.sleep(2)
			
			print( "HexBug " + str(i+1) + " pose = " + str(dum.getPose()[0:2]) )

			if dum.getPose()[0] != 0 or dum.getPose()[1] != 0:

				# If this hexbug is indeed on the map, add it to the neighboring hexbugs:
				dummyBots.append( dum  )
				dummyBotsAndItself.append( dum )
				m = m + 1
				pp = dum.getPose()[0:2]
				x.append(pp[0])
				y.append(pp[1])
			
			if ip - 1 == i:l
			#if vic_portF+i == ports[0]:
				Diff = i
		except: 
			print("moving on...")
	else:
		dum = vt.ViconTracker(i+1) # This is the current hexbug
		if dum.getPose()[0] != 0 or dum.getPose()[1] != 0:
			dummyBotsAndItself.append( dum )
		Diff = len(dummyBots)

print("n = " + str(n))
print("m = " + str(m))

numAll = len(dummyBots)+n

# Initialize the group synchronization
(numOfStates,memory,goalPoseForSync,offsetGoal,advance) = Sync2.initValues(autoMat,syncMat,numAll,numOfGroups,regionCenters,offsetVector)

print("numAll = " + str(numAll))

time.sleep(2)

dim = 4
pos = []
labels = []
a=[]

p = 1 
j = 1

x_cord = []
y_cord = []
pose = []
angleRay = [ 3*np.pi/2, np.pi/4 ]
j = 0 

atGoal = 0 
l = 0

# Initialize the swarm parameters to work for all the bots on the field:
obj = swarmParams.sysParams(numAll)
obj.initPose()
obj.goalPose()
obj.neighborRadius()

hexBugs[0].obj = obj 
hexBugs[0].indice = Diff
hexBugs[0].tolerance = obj.closeEnoughPose

print("Number of bots is: " + str(n+m+l))

obj.currentPose = np.matrix( np.zeros((2,numAll)) )
obj.goalPose = np.matrix( np.zeros((2,numAll)) )

poseAll = np.zeros([2,numAll])
poseAll = np.matrix(poseAll)

for l in range(n):
	hexBugs[l].objParams()

wallRange = 3.0
#MAP = np.matrix([[-wallRange,-wallRange,wallRange,-wallRange],[wallRange,-wallRange,wallRange,wallRange],
#			[wallRange,wallRange,-wallRange,wallRange],[-wallRange,wallRange,-wallRange,-wallRange]])

tNow = time.time()
tLoop = time.time()
array = []
lastUpdate = 0 
updateNext = 1
while time.time()-tNow < 1000:

	time.sleep(0.2)	

	# Determine the goal pose for thiss HexBug:
	(memory,goalPoseForSync,offsetGoal,advance) = Sync2.isReady(autoMat,syncMat,numAll,numOfGroups,numOfStates,memory,goalPoseForSync,offsetGoal,\
		poseAll,loopingIndex,advance,regionCenters,offsetVector)
	print( "goalPoseForSync=" + str(goalPoseForSync))
	print( "poseAll="+str(poseAll))
	
	# Update this Hexbugs goalpose
	hexBugs[0].goal[0] = goalPoseForSync[0,Diff]
	hexBugs[0].goal[1] = goalPoseForSync[1,Diff]
	obj.goalPose[:,Diff] = np.matrix(hexBugs[0].goal).reshape((2,1))
	print( "hexBug"+str(ip)+" goal is"+ str(hexBugs[0].goal[0:2]))

	ray = [] 
	for i in range(len(IPs)):
		
		time.sleep(0.2)
		# Include this HexBug in the list of all HexBugs on the field:
		dummyBots.insert(Diff,hexBugs[i].hexB)

		# Update the pose of all the bots in obj:
		updateDummies( dummyBots, Diff, obj )
		hexBugs[i].obj = obj

		# Remove this Hexbug from the list of all HexBugs on the field:
		dummyBots.pop(Diff)
		hexBugs[i].cali = False #Turn the calibration off that was used in the beginning
		hexBugs[i].updatePo() # Update this HexBugs pose
		
		# Upate the matrix poseall with the current pose of all the HexBugs
		l = 0
		for j in range(numAll):
			if (j != Diff ):
				poseAll[0,j] = dummyBots[l].getPose()[0]
				poseAll[1,j] = dummyBots[l].getPose()[1]
				l+=1
			else:
				poseAll[0,j] = hexBugs[i].r0[0]
				poseAll[1,j] = hexBugs[i].r0[1]
			obj.goalPose[:,j] = np.matrix(goalPoseForSync[:,j])

		statesNeighbor = np.array([]).reshape(2,0)
        indNeighbor = np.array([]).reshape(1,0)

        # Find the bots that are closest to this HexBug
		for j in range(numAll):
		        if j!=i+Diff:
		            statejTmp = np.array(np.matrix(poseAll)[:,j])
		            stateiTmp = np.array(np.matrix(poseAll)[:,i+Diff])
		            if np.linalg.norm(statejTmp-stateiTmp) <= obj.Dneighbor[i+Diff]:
		                statesNeighbor = np.hstack([statesNeighbor,statejTmp])
		                indNeighbor = np.hstack([indNeighbor,np.array([[j]])])

		poseAll = np.matrix(poseAll)
		statesNeighbor = np.matrix(statesNeighbor)
		indNeighbor = np.matrix(indNeighbor)

		# Update the current pose in the HexBug object
		obj.getCurrentPose(poseAll)

		if hexBugs[i].motionStart != 0:
			
			try:
				# Get an updated, intermediate goal point from the path planning algorithm
				waypoints_TmpTmp = pathPlanning.findPath(MAP,nodes,obj.currentPose[:,i+Diff],goalPoseForSync[:,Diff])
				obj.goalPose[:,Diff] = np.matrix(waypoints_TmpTmp)

				# Use the actual controller to determine the best orientation to proceed towards the goal
				vec = actualController(obj.currentPose[:,i+Diff],i+Diff,statesNeighbor,indNeighbor,obj,MAP)

				# Add the trajectory information into the array to be outputted at the end of the code
				array.append(np.array([vec[0],vec[1],obj.currentPose[0,Diff],obj.currentPose[1,Diff],hexBugs[i].r0[2],obj.goalPose[0,Diff],obj.goalPose[1,Diff]]))

				# Normalize the vector from the controller
				vec = np.array( [ vec[0], vec[1] ] ).reshape((2,))
				nm = np.linalg.norm(vec) 
				if (nm != 0):
					vec = vec/nm 

				# Calculate the orientation from the normalized vector
				b2, theta, b1 = hexBugs[i].cordToRad( np.array([0,0]).reshape((2,)), vec, np.pi)

				chan = -(hexBugs[i].r0[2] - b1)
				if np.abs(chan) >= np.pi:

					temp = chan

					if np.sign( chan ) == -1:
						chan += 2 * np.pi 

					else:

						chan -= 2 * np.pi 

			except:
					vec = np.array([ hexBugs[i].goal[0] - hexBugs[i].r0[0], hexBugs[i].goal[1] - hexBugs[i].r0[1] ]).reshape((2,))
					vec = vec/ np.linalg.norm(vec)				
					#b1 = hexBugs[i].r0[2]
					#theta = 0;
					#vec =  np.array([0,0])
					b2, theta, b1 = hexBugs[i].cordToRad( np.array([0,0]).reshape((2,)), vec, np.pi)
					chan = -(hexBugs[i].r0[2] - b1)
					if np.abs(chan) >= np.pi:

						temp = chan

						if np.sign( chan ) == -1:
							chan += 2 * np.pi 

						else:

							chan -= 2 * np.pi 
					print( "Dead Lock!!!" )
					vec = np.array([0,0])

			curDis = np.sqrt( (hexBugs[i].r0[0]-hexBugs[i].goal[0])**2 + (hexBugs[i].r0[1]-hexBugs[i].goal[1])**2 )
			print( "Current Distance: " + str(curDis))
			if curDis < hexBugs[i].tolerance or hexBugs[i].excCount > 5 :
				
				if hexBugs[i].curInd+1 >= 100: #len(hexBugs[i].goal):
					atGoal += 1 
					hexBugs[i].close()
				elif hexBugs[i].excCount > 5:
					atGoal += 1
					#print( hexBugs[i].name + " Connection lost" )
					hexBugs[i].close()
					hexBugs[i] = hx.hexBug( IPs[i], 'HexBug' + str(i+1), hexBugs[i].UDP_PORT, hexBugs[i].vic_port)
				else: 
					print(hexBugs[i].name + " waiting for group..")
					#hexBugs[i].soc.sendall(b's')
			else:
				print( hexBugs[i].name + " angle position input: " + str(b1) )
				print( hexBugs[i].name + " current angle: " +str( hexBugs[i].r0[2]))
				if not (vec[0]==0 and vec[1]==0):				
					if np.abs(theta) > hexBugs[i].angTol:
						timeVal = hexBugs[i].rig_lef(chan,b1)
					if ( time.time()-lastUpdate > updateNext ) :
						hexBugs[i].fwd_back(1)
						lastUpdate = time.time()
					timeVal = 0
				else:
					hexBugs[i].soc.sendall(b's')
					timeVal = 0

path1 = r"Data\ "

f = open( path1 + 'controllerOutputHexBug' + str(ip) + 'Date' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) +'.csv', 'w')

writer = csv.writer(f, delimiter=',')
labs = []
for i in range( len( hexBugs ) ):
	labs.append( ["Vec X", "Vec Y", "HexBug Pose X", "HexBug Pose Y", "HexBug Orientation (rad)", "Goal Pose X", "Goal Pose Y"] )

labs = np.concatenate(labs, axis=0)
writer.writerow( labs )
for i in range( len(array) ):
	writer.writerow(array[i])
